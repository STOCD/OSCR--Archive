import numpy
from re import search as re_search
from datetime import timedelta

from .datamodels import Combat, PlayerTableRow

HANDLE_REGEX = '^P\\[.+?@.+?(?P<handle>@.+?)\\]$'

def analyze_shallow(combat:Combat, settings):
    '''
    Analyzes the provided combat for overview data (table listing general player stats and graphs)
    '''
    graph_resolution = settings['graph_resolution']
    graph_timedelta = timedelta(seconds=graph_resolution)
    last_graph_time = combat.log_data[0].timestamp
    graph_points = 1
    combat.table = list()
    player_dict = dict()
    for line in combat.log_data:
        # manage entites
        player_attacks = line.owner_id.startswith('P')
        player_attacked = line.target_id.startswith('P')
        if not player_attacks and not player_attacked:
            continue
        attacker = None
        target = None
        crit_flag, miss_flag, _, kill_flag = get_flags(line.flags)
        if player_attacks:
            if not line.owner_id in player_dict:
                player_dict[line.owner_id] = PlayerTableRow(line.owner_name, 
                        get_handle_from_id(line.owner_id))
                player_dict[line.owner_id].combat_start = line.timestamp
            attacker = player_dict[line.owner_id]
            attacker.combat_end = line.timestamp
        if player_attacked:
            if not line.target_id in player_dict:
                player_dict[line.target_id] = PlayerTableRow(line.target_name,
                        get_handle_from_id(line.target_id))
                player_dict[line.target_id].combat_start = line.timestamp
            target = player_dict[line.target_id]
            target.combat_end = line.timestamp

        # get table data
        if miss_flag:
            try:
                attacker.misses += 1
            except AttributeError:
                pass
        if kill_flag:
            try:
                target.deaths += 1
            except AttributeError:
                pass
        
        if ((line.type == 'Shield' and line.magnitude < 0 and line.magnitude2 >= 0) 
                        or line.type == 'HitPoints'):
            try:
                attacker.total_heals += abs(line.magnitude)
                attacker.heal_num += 1
                if crit_flag:
                    attacker.heal_crit_num += 1
            except AttributeError:
                pass
        else:
            magnitude = abs(line.magnitude)
            try:
                target.total_damage_taken += magnitude
                target.attacks_in_num += 1
            except AttributeError:
                pass
            try:
                attacker.total_attacks += 1
                attacker.total_damage += magnitude
                attacker.damage_buffer += magnitude
                if crit_flag:
                    attacker.crit_num += 1
                if magnitude > attacker.max_one_hit:
                    attacker.max_one_hit = magnitude
                if not line.type == 'Shield' and not miss_flag:
                    if line.magnitude != 0 and line.magnitude2 != 0:
                        attacker.resistance_sum += line.magnitude / line.magnitude2
                        attacker.hull_attacks += 1
            except AttributeError:
                pass
        
        # update graph
        if line.timestamp - last_graph_time >= graph_timedelta:
            for player in player_dict.values():
                player.DMG_graph_data.append(player.damage_buffer)
                player.damage_buffer = 0.0
                player.graph_time.append(graph_points * graph_resolution)
            graph_points += 1
            last_graph_time = line.timestamp
    
    for player in player_dict.values():
        player.combat_time = (player.combat_end - player.combat_start).total_seconds()
        successful_attacks = player.total_attacks - player.misses
        try:
            player.debuff = player.resistance_sum / player.hull_attacks * 100
        except ZeroDivisionError:
            player.debuff = 0.0
        try:
            player.DPS = player.total_damage / player.combat_time
        except ZeroDivisionError:
            player.DPS = 0.0
        if successful_attacks > 0:
            player.crit_chance = player.crit_num / successful_attacks * 100
        else:
            player.crit_chance = 0
        try:
            player.heal_crit_chance = player.heal_crit_num / player.heal_num * 100
        except ZeroDivisionError:
            player.heal_crit_chance = 0.0

        player.graph_time = tuple(map(lambda x: round(x, 1), player.graph_time))
        DPS_data = numpy.array(player.DMG_graph_data, dtype=numpy.float64).cumsum()
        player.DPS_graph_data = tuple(DPS_data / player.graph_time)
        
    combat.table, combat.graph_data = create_overview(player_dict)

def create_overview(player_dict:dict) -> list[list]:
    '''
    converts dictionary containing player data to table data for the front page
    '''
    table = list()
    total_damage = 0
    total_damage_taken = 0
    total_attacks = 0
    total_heals = 0

    DPS_graph_data = dict()
    DMG_graph_data = dict()
    graph_time = dict()

    for player in player_dict.values():
        total_damage += player.total_damage
        total_damage_taken += player.total_damage_taken
        total_attacks += player.attacks_in_num
        total_heals += player.total_heals

    for player in player_dict.values():
        try:
            player.damage_share = player.total_damage / total_damage * 100
        except ZeroDivisionError:
            player.damage_share = 0.0
        try:
            player.taken_damage_share = player.total_damage_taken / total_damage_taken * 100
        except ZeroDivisionError:
            player.taken_damage_share = 0.0
        try:
            player.attacks_in_share = player.attacks_in_num / total_attacks * 100
        except ZeroDivisionError:
            player.attacks_in_share = 0.0
        try:
            player.heal_share = player.total_heals / total_heals * 100
        except ZeroDivisionError:
            player.heal_share = 0.0
        table.append((*player,))

        DPS_graph_data[player.handle] = player.DPS_graph_data
        DMG_graph_data[player.handle] = player.DMG_graph_data
        graph_time[player.handle] = player.graph_time
    table.sort(key=lambda x: x[0])
    return (table, (graph_time, DPS_graph_data, DMG_graph_data))

def get_handle_from_id(id_str:str) -> str:
    '''
    returns player handle from is string
    '''
    handle = re_search(HANDLE_REGEX, id_str)
    if handle is None:
        return ''
    return handle.group('handle')


def get_flags(flag_str:str) -> tuple[bool]:
    '''
    Returns flags from flag field of log line.

    Return: (critical_hit, miss, flank, kill)
    '''
    critical_hit = 'Critical' in flag_str
    miss = 'Miss' in flag_str
    flank = 'Flank' in flag_str
    kill = 'Kill' in flag_str
    return (critical_hit, miss, flank, kill)