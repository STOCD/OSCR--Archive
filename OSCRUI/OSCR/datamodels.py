from typing import Optional
from datetime import datetime
from collections import namedtuple


LogLine = namedtuple('LogLine', 
        ('timestamp',
        'owner_name', 
        'owner_id', 
        'source_name', 
        'source_id', 
        'target_name', 
        'target_id', 
        'event_name', 
        'event_id', 
        'type', 
        'flags', 
        'magnitude', 
        'magnitude2'))

class PlayerTableRow():
    '''
    Contains a single row of data
    '''
    __slots__ = ('name', 'handle', 'combat_time', 'DPS', 'total_damage', 'crit_chance', 'max_one_hit', 
            'debuff', 'damage_share', 'taken_damage_share', 'attacks_in_share', 'total_heals', 
            'heal_crit_chance', 'heal_share', 'deaths', 'heal_crit_num', 'heal_num', 'crit_num', 
            'total_damage_taken', 'attacks_in_num', 'total_attacks', 'hull_attacks', 'resistance_sum', 
            'misses', 'DMG_graph_data', 'DPS_graph_data', 'graph_time', 'damage_buffer', 'combat_start',
            'combat_end')
    
    def __init__(self, name:str, handle:str):
        self.name: str = name
        self.handle: str = handle
        self.combat_time: float = 0.0
        self.DPS: float = 0.0
        self.total_damage: float = 0.0
        self.crit_chance: float = 0.0
        self.max_one_hit: float = 0.0
        self.debuff: float = 0.0
        self.damage_share: float = 0.0
        self.taken_damage_share: float = 0.0
        self.attacks_in_share: float = 0.0
        self.total_heals: float = 0.0
        self.heal_crit_chance: float = 0.0
        self.heal_share: float = 0.0
        self.deaths: int = 0

        self.heal_crit_num: int = 0
        self.heal_num: int = 0
        self.crit_num: int = 0
        self.total_damage_taken: float = 0.0
        self.attacks_in_num: int = 0
        self.total_attacks: int = 0
        self.hull_attacks: int = 0
        self.resistance_sum: float = 0.0
        self.misses: int = 0

        self.DMG_graph_data: list[float] = list()
        self.DPS_graph_data: list[float] = list()
        self.graph_time: list[float] = list()
        self.damage_buffer: float = 0.0
        self.combat_start: datetime = None
        self.combat_end: datetime = None

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.name}{self.handle}>'
    
    def __len__(self) -> int:
        return 15
    
    def __getitem__(self, position):
        match position:
            case 0: return self.name
            case 1: return self.handle
            case 2: return self.combat_time
            case 3: return self.DPS
            case 4: return self.total_damage
            case 5: return self.crit_chance
            case 6: return self.max_one_hit
            case 7: return self.debuff
            case 8: return self.damage_share
            case 9: return self.taken_damage_share
            case 10: return self.attacks_in_share
            case 11: return self.total_heals
            case 12: return self.heal_crit_chance
            case 13: return self.heal_share
            case 14: return self.deaths
            case _: raise StopIteration()

class TableRow():
    '''
    Contains data of a single row. Can have child rows.
    '''
    __slots__ = ('_row_data', '_children')

    def __init__(self, data:Optional[list] = None, children:Optional[list] = None) -> None:
        self._row_data = list()
        self._children = list()
        if isinstance(data, list):
            self._row_data = data
        if isinstance(children, list):
            self._children = children

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} - {self._row_data} - {len(self._children)} child rows>'
    
    def __len__(self) -> int:
        return len(self._row_data)
    
    def __getitem__(self, index:int):
        try:
            return self._row_data[index]
        except IndexError:
            raise IndexError
    
    def __setitem__(self, index:int, value) -> None:
        self._row_data[index] = value
    
    @property
    def children(self):
        return self._children
    
    @property
    def row_data(self):
        return self
    
    @row_data.setter
    def row_data(self, full_row:list):
        self._row_data = full_row

class Combat():
    '''
    Contains a single combat including raw log lines, map and combat information and shallow parse results.
    '''
    __slots__ = ('log_data', '_map', 'date_time', 'table', 'graph_data')

    def __init__(self, log_lines:Optional[list[LogLine]] = None) -> None:
        self.log_data = log_lines
        self._map = None
        self.date_time = None
        self.table = None
        self.graph_data = None

    @property
    def map(self) -> str:
        if self._map is None:
            return 'Combat'
        return self._map
    
    @map.setter
    def map(self, map_name):
        self._map = map_name

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} - Map: {self.map} - Datetime: {self.date_time}>'
    
    def __gt__(self, other):
        if not isinstance(other, Combat):
            raise TypeError(f'Cannot compare {self.__class__.__name__} to {other.__class__.__name__}')
        if isinstance(self.date_time, datetime) and isinstance(self.date_time, datetime):
            return self.date_time > other.date_time
        if not isinstance(self.date_time, datetime) and isinstance(self.date_time, datetime):
            return False
        if isinstance(self.date_time, datetime) and not isinstance(other.date_time, datetime):
            return True