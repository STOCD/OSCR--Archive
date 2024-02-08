from datetime import timedelta
import os

from .datamodels import Combat, LogLine
from .iofunc import MAP_IDENTIFIERS_EXISTENCE
from .iofunc import get_combat_log_data, split_log_by_lines, reset_temp_folder
from .utilities import to_datetime, datetime_to_display
from .baseparser import analyze_shallow

TABLE_HEADER = ('Combat Time', 'DPS', 'Total Damage', 'Crit Chance', 'Max One Hit', 'Debuff', 'Damage Share',
        'Taken Damage Share', 'Attacks-in Share', 'Total Heals', 'Heal Crit Chance', 'Heals Share', 'Deaths')

class OSCR():

    version = '2024.02b70'

    def __init__(self, log_path:str = None, settings:dict = None):
        self.log_path = log_path
        self.combats = list()
        self.combats_pointer = None
        self.excess_log_lines = list()
        self.combatlog_tempfiles = list()
        self.combatlog_tempfiles_pointer = None
        self._settings = {
            'combats_to_parse': 10,
            'seconds_between_combats': 100,
            'excluding_event_ids': ['Autodesc.Combatevent.Falling'],
            'graph_resolution': 0.2,
            'templog_folder_path': f'{os.path.dirname(os.path.abspath(__file__))}\\~temp_log_files'
        }
        if settings is not None:
            self._settings.update(settings)

    @property
    def analyzed_combats(self) -> tuple[str]:
        '''
        Contains tuple with available combats.
        '''
        return tuple([f'{c.map} {datetime_to_display(c.date_time)}' for c in self.combats])
    
    @property
    def active_combat(self) -> Combat | None:
        '''
        Combat currently active (selected).
        '''
        if self.combats_pointer is not None:
            return self.combats[self.combats_pointer]
        else:
            return None
    
    @property
    def navigation_up(self) -> bool:
        '''
        Indicates whether newer combats are available, but not yet analyzed.
        '''
        if self.combatlog_tempfiles_pointer is None:
            return False
        return self.combatlog_tempfiles_pointer < len(self.combatlog_tempfiles) - 1
    
    @property
    def navigation_down(self) -> bool:
        '''
        Indicates whether older combats are available, but not yet analyzed.
        '''
        if len(self.excess_log_lines) > 0:
            return True
        if self.combatlog_tempfiles_pointer is None:
            return False
        return self.combatlog_tempfiles_pointer > 0

    def identfy_map(self, entity_id:str) -> str | None:
        '''
        Identify map by checking whether the entity supplied identifies a map. Returns map name or None.
        '''
        try:
            clean_entity_id = entity_id.split(' ', maxsplit=1)[1].split(']', maxsplit=1)[0]
        except IndexError:
            return None
        if clean_entity_id in MAP_IDENTIFIERS_EXISTENCE:
            return MAP_IDENTIFIERS_EXISTENCE[clean_entity_id]
        return None      

    def analyze_log_file(self, total_combats:int | None = None, extend:bool = False, 
            log_path:str | None = None):
        '''
        Analyzes the combat at self.log_path and replaces self.combats with the newly parsed combats.
        
        Parameters:
        - :param total_combats: holds the number of combats that should be in self.combats after the method is 
        finished.
        - :param extend: extends the list of current combats to match the number of total_combats by analyzing
        excess_log_lines
        - :param log_path: specify log path different from self.log_path to be analyzed. Has no effect when
        parameter extend is True
        '''
        if self.log_path is None and log_path is None:
            raise AttributeError('"self.log_path" or parameter "log_path" must contain a path to a log file.')
        if total_combats is None:
            total_combats = self._settings['combats_to_parse']
        if extend:
            if total_combats <= len(self.combats):
                return
            log_lines = self.excess_log_lines
            self.excess_log_lines = list()
        else:
            if log_path is not None:
                log_lines = get_combat_log_data(log_path)
            else:
                log_lines = get_combat_log_data(self.log_path)
            log_lines.reverse()
            self.combats = list()
            self.excess_log_lines = list()
        combat_delta = timedelta(seconds=self._settings['seconds_between_combats'])
        current_combat_lines = list()
        current_combat = None
        map_identified = False
        last_log_time = to_datetime(log_lines[0].split('::')[0]) + 2 * combat_delta

        for line_num, line in enumerate(log_lines):
            time_data, attack_data = line.split('::')
            log_time = to_datetime(time_data)
            if last_log_time - log_time > combat_delta:
                if current_combat is not None:
                    if not (len(current_combat_lines) < 20 
                            and current_combat_lines[0].event_id in self._settings['excluding_event_ids']):
                        current_combat_lines.reverse()
                        current_combat.log_data = current_combat_lines
                        current_combat.date_time = last_log_time
                        self.combats.append(current_combat)
                    if len(self.combats) == self._settings['combats_to_parse']:
                        self.excess_log_lines = log_lines[line_num:]
                        return
                current_combat_lines = list()
                current_combat = Combat()
                map_identified = False
            splitted_line = attack_data.split(',')
            current_line = LogLine(log_time, 
                    *splitted_line[:10],
                    float(splitted_line[10]),
                    float(splitted_line[11])
                    )
            if not map_identified:
                current_map = self.identfy_map(current_line.target_id)
                if current_map is not None:
                    current_combat.map = current_map
                    map_identified = True
   
            last_log_time = log_time
            current_combat_lines.append(current_line)
    
        current_combat_lines.reverse()
        current_combat.log_data = current_combat_lines
        current_combat.date_time = last_log_time
        self.combats.append(current_combat)

    def analyze_massive_log_file(self, total_combats:int | None = None):
        '''
        Analyzes the combat at self.log_path and replaces self.combats with the newly parsed combats.
        Used to analyze log files larger than around 500000 lines. Wraps around self.analyze_log_file.

        Parameters:
        - :param total_combats: holds the number of combats that should be in self.combats after the method is 
        finished.
        '''
        if self.log_path is None:
            raise AttributeError('"self.log_path" must contain a path to a log file.')
        temp_folder_path = self._settings['templog_folder_path']
        reset_temp_folder(temp_folder_path)
        self.combatlog_tempfiles = split_log_by_lines(self.log_path, temp_folder_path, approx_lines_per_file= 80000)
        self.combatlog_tempfiles_pointer = len(self.combatlog_tempfiles) - 1
        self.analyze_log_file(total_combats, 
                log_path=self.combatlog_tempfiles[self.combatlog_tempfiles_pointer])
        
    def navigate_log(self, direction:str = 'down'):
        '''
        Analyzes earlier combats when direction is "down"; loads earlier templog file if current file is
        exhausted; loads later combatlog file if direction is "up".
        '''
        if direction == 'down' and self.navigation_down:
            if self.combatlog_tempfiles_pointer is None:
                self.analyze_log_file(extend=True)
            else:
                self.combatlog_tempfiles_pointer -= 1
                self.analyze_log_file(log_path=self.combatlog_tempfiles[self.combatlog_tempfiles_pointer])
        elif direction == 'up' and self.navigation_up:
           self.combatlog_tempfiles_pointer += 1
           self.analyze_log_file(log_path=self.combatlog_tempfiles[self.combatlog_tempfiles_pointer])


    def shallow_combat_analysis(self, combat_num:int) -> tuple[list]:
        '''
        Analyzes combat from currently available combats in self.combat.

        Parameters:
        - :param combat_num: index of the combat in self.combats

        :return: tuple containing the overview table, DPS graph data and DMG graph data
        '''
        try:
            analyze_shallow(self.combats[combat_num], self._settings)
            self.combats_pointer = combat_num
            return (self.combats[combat_num].table,
                    self.combats[combat_num].graph_data)
        except IndexError:
            raise AttributeError(f'Combat #{combat_num} you are trying to analyze has not been isolated yet.'
                                 f'Number of isolated combats: {len(self.combats)} -- '
                                 'Use OSCR.analyze_log_files() with appropriate arguments first.')

if __name__ == '__main__':
    test_parser = OSCR('combatlog.log')
    test_parser.analyze_log_file()
    #output = test_parser.shallow_combat_analysis(2)
    #print(output)
    print('end')
    
                


            



    

    
