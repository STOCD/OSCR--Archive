import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from settings import DEFAULT_INTERVAL, EXTERNAL, TIME_BETWEEEN_COMBAT, WEAPONS, EXCLUDE_DAMAGE, EXCLUDE_ATTACKS
from core import instance
#from core import player
import numpy as np
import math

parse = None
date_times = None
mag2 = None

def read_parse(filepath):
    global parse
    global date_times
    global mag2
    parse = pd.read_csv(filepath, names=["header","player_id","pet_name","pet_id","target_name","target_id","activity_source","activity_id","type","flag","mag1","mag2"])
    parse[['timestamp','source']] = parse['header'].str.split('::',expand=True)
    parse['timestamp'] = pd.to_datetime(parse['timestamp'],format='%y:%m:%d:%H:%M:%S.%f')
    date_times = parse['timestamp'].to_list()
    mag2 = parse['mag2'].to_list()


def get_pet_slice(instance,player="",flag=""):
    #Filter the parse down to the indicated instance
    if instance.end == -1:
        slice = parse.loc[instance.start:]
    else:
        slice = parse.loc[instance.start:instance.end]

    if player != "":
        slice = slice[slice.source==player]


    if flag == "":
        return slice

    healing_sources = slice[(slice.type == 'HitPoints') | ((slice.type == 'Shield')) & (slice.mag1 < 0) & (slice.mag2 >=0) & (slice.source == player)].activity_source.unique()
    damage_sources = slice[(~slice.activity_source.isin(healing_sources)) & (~slice.activity_source.isin(EXCLUDE_DAMAGE))].activity_source.unique()
    pet_sources = get_pet_list(instance,player)
    
    if flag == 'healing':
        slice = slice[(slice.pet_name.isin(pet_sources)) & (slice.activity_source.isin(healing_sources))]
    elif flag == 'damage':
        slice = slice[(slice.pet_name.isin(pet_sources)) & (~slice.target_name.isin(get_player_list(instance))) & (slice.activity_source.isin(damage_sources))]

    return slice

def get_slice(instance=None,player=None,flag=None):
    
    if instance == None:
        return
    #Filter the parse down to the indicated instance
    if instance.end == -1:
        slice = parse.loc[instance.start:]
    else:
        slice = parse.loc[instance.start:instance.end]

    if player:
        slice = slice[slice.player_id==player]

    healing_sources = slice[(slice.type == 'HitPoints') | ((slice.type == 'Shield')) & (slice.mag1 < 0) & (slice.mag2 >=0)].activity_source.unique()
    damage_sources = slice[(slice.mag1 >=0) & (~slice.activity_source.isin(EXCLUDE_DAMAGE))].activity_source.unique()

    if flag == 'healing':
        slice = slice[(slice.activity_source.isin(healing_sources)) & (slice.mag1 < 0)]
    elif flag == 'damage':
        slice = slice[(~slice.target_name.isin(get_player_list(instance))) & (slice.activity_source.isin(damage_sources))]               

    return slice

        
def get_combat_instances():
    time_diff = [(date_times[i+1] - date_times[i]).seconds for i in range(0,len(parse)-1)]
    start_times = [0] + [time_diff.index(i)+1 for i in time_diff if i >= TIME_BETWEEEN_COMBAT]
    end_times = [i-1 for i in start_times[1:]] + [-1]
    return_markers = []
    for i in range(0,len(start_times)):
        return_markers.append(instance(start_times[i],end_times[i]))

    return return_markers

def get_player_list(instance):
    slice = get_slice(instance)
    return slice[slice.player_id.str.startswith('P',na=False)].player_id.unique()

def get_pet_list(instance,player):
    player_list = get_player_list(instance)
    enemy_list = get_enemy_list(instance)
    slice = get_slice(instance,player,None)
    print(player)
    pet_list = []
    pets = slice[(slice.source==player) & (~slice.pet_name.isin(enemy_list)) & (~slice.pet_name.isin(player_list)) & (~slice['pet_name'].isnull())].pet_name.unique()
    for pet in pets:
        if (not any(weapon in str(pet) for weapon in WEAPONS.split('|'))) & (not any(ability in str(slice[slice.pet_name==pet].activity_source.unique()) for ability in EXTERNAL.split('|'))):
            pet_list.append(pet)
            
    return(pet_list)

def get_entity_list(instance):
    return get_slice(instance).source.unique()

def get_enemy_list(instance):
    slice = get_slice(instance,None,None)
    player_list = get_player_list(instance)
    return slice[(slice['flag'] != 'Miss') & (slice.source != '') & (~slice.source.isin(player_list))].source.unique()

def get_id_list(instance,player):
    player_id = get_slice(instance,player,'damage').iloc[0].player_id
    pet_id_list = get_pet_slice(instance,player).pet_id.unique()
    return np.append(pet_id_list,player_id)

def get_combat_time(instance,player,slice):
    try:
        start_datetime = slice.iloc[0].timestamp
        end_datetime = slice.iloc[-1].timestamp
    except Exception:
        return 0

    return((end_datetime - start_datetime).total_seconds())

def get_flags(slice):
    return slice.flag.unique()

def parse_flags(flag):
    
    if type(flag) == float:
        return 'none'
    else:
        return flag.split('|')

def get_damage(instance,player,slice):
    return sum(abs(slice.mag1))

def get_damage_itemized(instance,player):
    slice = get_slice(instance,player,'damage')
    activities = slice.activity_source.unique()
    for activity in activities:
        print(str(activity) + ": " + str(sum(abs(slice[slice.activity_source==activity].mag1))))

def get_dps(instance,player,slice):
    dmg = get_damage(instance,player,slice)
    tme = get_combat_time(instance,player,slice)

    if tme == 0:
        return 0
    else:
        return dmg/tme

def get_max_one_hit(slice):
    return abs(slice['mag1']).max()

def get_hull_damage(slice):
    slice = slice[slice.type != 'Shield']
    return sum(abs(slice.mag1))

def get_shield_damage(slice):
    slice = slice[slice.type == 'Shield']
    return sum(abs(slice.mag1))

def get_attack(activity,slice):
    """
    
    Args:
        activity: a string that specifies the name of the damage source
        slice: a slice object

    Returns:
        the number of attacks made by the specified player with the specified activity source
    """
    if str(activity) in EXCLUDE_ATTACKS:
        return 0

    index_list = slice[slice.activity_source==activity].index.to_numpy()
    shield_index_list = slice[(slice.activity_source==activity) & (slice.type=='Shield')].index.to_list() 
    
    return sum([int(((i in shield_index_list) & (mag2[i] == 0)) | (i not in shield_index_list)) for i in index_list])

def get_attacks_in(instance,player,slice):
    return 0

def get_attacks(instance,player,slice):
    activities = slice.activity_source.unique()
    total = 0
    for activity in activities:
        total += get_attack(instance,player,activity,slice)

    return total

def get_hit_rate(instance,player,slice,source=None):
    print(player)
    if source:
        attacks = get_attack(instance,player,source,slice)
        if attacks == 0:
            return 0
        misses = len(slice[(slice.activity_source == source) & (slice.flag.str.contains('Miss'))].index)
        #print(str(activity) + ":" + "{:.2%}".format((attacks-misses)/attacks))
        return ((attacks-misses)/attacks)
    else:
        attacks = get_attacks(instance,player,slice)
        if attacks == 0:
            return 0
        misses = len(slice[(slice.flag.str.contains('Miss',na=False))].index)
        print("misses: " + str(misses))
            #print(str(activity) + ":" + "{:.2%}".format((attacks-misses)/attacks))
            
        return (attacks-misses)/attacks                

def get_crit_percentage(instance,player,source=None):
    slice = get_slice(instance,player,'damage')
    if source:
        attacks = get_attack(instance,player,source,slice) * get_hit_rate(instance,player,slice,source)
        if attacks == 0:
            return 0
        crits = len(slice[(slice.activity_source == source) & (slice.flag.str.contains('Critical'))].index)
        return "{:.2%}".format(crits/attacks)
    else:
        attacks = get_attacks(instance,player,slice) * get_hit_rate(instance,player,slice)
        if attacks == 0:
            return 0
        crits = len(slice[(slice.flag.str.contains('Critical',na=False))].index)

        return crits/attacks
    
def get_crit_percentage_itemized(instance,player,slice,activity=""):
    activities = slice.activity_source.unique()
    for activity in activities:
        get_crit_percentage(instance,player,slice,activity)

    return get_crit_percentage(instance,player,slice)

def get_flank_percentage(instance,player,slice,activity=""):
    if activity != "":
        attacks = get_attack(instance,player,activity,slice) * get_hit_rate(instance,player,activity,slice)
        if attacks == 0:
            return 0
        flanks = len(slice[(slice.activity_source == activity) & (slice.flag.str.contains('Flank'))].index)
        return str(activity) + ":" + "{:.2%}".format(flanks/attacks)
    else:
        attacks = get_attacks(instance,player,slice) * get_hit_rate(instance,player,slice)
        if attacks == 0:
            return 0
        flanks = len(slice[(slice.flag.str.contains('Flank',na=False))].index)

        return flanks/attacks

def get_kills(instance,player):
    slice = get_slice(instance,player,'damage')
    return len(slice[(slice.flag.str.contains('Kill',na=False))].index)

def get_base_damage(instance,player):
    return

def get_base_hull_damage(instance,player):
    return

def get_base_shield_damage(instance,player):
    return

def get_max_crit(instance,player):
    slice = get_slice(instance,player, 'damage')
    return abs((slice[(slice.flag.str.contains('Critical',na=False))].mag1)).max()

def get_max_hit(instance,player):
    return

def get_avg_crit(instance,player,source):
    return

def get_avg_hit(instance,player):
    slice = get_slice(instance,player,'damage')
    dmg = get_damage(instance,player,slice)
    attacks = get_attacks(instance,player,slice)
    return (dmg/attacks)

def get_percentage_damage_out(instance,player):
    player_list = get_player_list(instance)
    total_damage = 0
    player_damage = 0
    for p in player_list:
        damage = get_damage(instance,p,get_slice(instance,p,'damage'))
        total_damage += damage
        if p == player:
            player_damage = damage

    return player_damage/total_damage


def get_damage_taken(instance,player):
    slice = get_slice(instance)
    types = slice.type.unique()
    damge_to_player = 0

    for type in types:
        if isinstance(type,float):
            continue
        dmg = sum(abs(slice[((slice.target_name==player) | (slice.pet_name==player)) & (slice.type==type) & ~((slice.type == 'HitPoints') | ((slice.type == 'Shield')) & (slice.mag1 < 0) & (slice.mag2 >=0))].mag1))
        damge_to_player += dmg
        
    return damge_to_player

def get_percentage_damage_taken(instance,player):
    return 0


def get_percentage_attacks_taken(instance,player):
    return

def get_healing_out(instance,player):
    return

def get_healing_out_itemized(instance,player):
    slice = get_slice(instance,player,'healing')
    activities = slice.activity_source.unique()
    for activity in activities:
        print(str(activity) + ": " + str(sum(abs(slice[slice.activity_source==activity].mag1))))

def get_percentage_healing_out(instance,player):
    
    return

def get_max_heal(instance,player):
    slice = get_slice(instance,player,'healing')
    return abs(slice['mag1']).max()


def get_percentage_heal_crit(instance,player):
    slice = get_slice(instance,player,'healing')
    all_heals = len(slice.index)
    crit_heals = len(slice[(slice.flag.str.contains('Critical',na=False))].index)
    return "{:.2%}".format((crit_heals/all_heals))

def get_deaths(instance,player):
    slice = get_slice(instance,None,None)
    slice = slice[slice.target_name==player]
    deaths = len(slice[(slice.flag.str.contains('Kill',na=False))].index)
    return deaths

def get_damage_per_interval(slice,instance,player,interval=DEFAULT_INTERVAL,source=None, mask=False, offset=False):
    if source:
        slice = slice[slice.activity_source==source]

    if offset:
        combat_start_time = pd.to_datetime(get_slice(instance,player,'damage').timestamp.values[0])
    else:
        combat_start_time = date_times[instance.start]

    combat_end_time = date_times[instance.end]
    combat_intervals = pd.date_range(start=combat_start_time,end=combat_end_time,freq=interval).to_series().index.values
    series = slice.groupby('timestamp')['mag1'].apply(lambda c: c.abs().sum())
    index = series.index
    values = series.values
    damage_index = np.asarray([np.where(combat_intervals == i)[0][0] for i in index])
    damage = [0 if i not in damage_index else values[np.where(damage_index==i)[0][0]] for i in range(len(combat_intervals))]
    damage = np.add.reduceat(damage, np.arange(0,len(damage),10))

    if mask:
        damage = [0 if i == 0 else 1 for i in damage]

    return damage

def plot_damage(instance, player, interval=DEFAULT_INTERVAL, source=None):
    slice = get_slice(instance,player,'damage')
    d = get_damage_per_interval(slice,instance,player,interval,source)
    plt.bar(range(0,len(d)),d)


def plot_dps(instance,player, interval=DEFAULT_INTERVAL,source=None, mask=False):
    slice = get_slice(instance,player,'damage')

    if source:
        slice = slice[slice.activity_source==source]

    damage = get_damage_per_interval(slice,instance,player,interval,None,False,True)
    offset = get_combat_offset(instance,player)
    dps = [0 for i in range(offset[0])] + [sum(damage[:(i+1)])/(i+1) for i in range(len(damage)-offset[1])]
    plt.plot(dps)
    return

def plot_dps_summary(instance):
    players = get_player_list(instance)
    dps = {players[i]:get_dps(instance,players[i],get_slice(instance,players[i],'damage')) for i in range(len(players))}
    dps = sorted(dps.items(), key=lambda x: x[1], reverse=True)
    names,numbers = list(zip(*dps))
    plt.barh(names,numbers)
    plt.show()
    return

def get_combat_offset(instance,player):
    combat_start = date_times[instance.start]
    combat_end = date_times[instance.end]
    player_times = pd.to_datetime(get_slice(instance,player,'damage').timestamp.values)
    player_start = player_times[0]
    player_end = player_times[-1]
    return (math.floor((player_start - combat_start).total_seconds()), math.ceil((combat_end - player_end).total_seconds()))





    

    
    
