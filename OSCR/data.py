import os
from multiprocessing import Pipe, Process
from typing import Union
import json
from re import sub as re_sub
import sys

from PyQt6.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt6.QtCore import QAbstractTableModel, Qt, QSortFilterProxyModel

from OSCR import OSCR
from OSCR.lib import clean_player_id, filtered_ability, resize_tree_table, get_entity_num, analysis_parser
from OSCR.lib import CustomThread, StandardItem, std_item_generator
from OSCR.ui.widgets import ARIGHT, ACENTER, AVCENTER

TABLE_HEADER_CONVERSION = {
    'combatTime': 'Combat Time',
    'DPS': 'DPS',
    'Total Damage': 'Total Damage',
    'CritH': 'Crit Chance', # %
    'MaxOneHit': 'Max One Hit',
    '%debuff': 'Debuff', # %
    '%damage': 'Damage Share', # %
    '%damage taken': 'Taken Damage Share', # %
    '%atks-in': 'Attacks-in Share', # %
    'total heals': 'Total Heals',
    'healCrtH': 'Heal Crit Chance', # %
    '% healed': 'Heals Share', # %
    'deaths': 'Deaths'
}

DAMAGE_HEADER = ['', 'Damage', 'DPS', 'Max One Hit', 'Crits', 'Flanks', 'Attacks', 'Misses', 'Crit Chance',
        'Accuracy', 'Flank Rate', 'Kills', 'Hull Damage', 'Shield Damage', 'Resistance', 'Hull Attacks',
        'Final Resistance']

HEAL_HEADER = ['', 'Total Heal', 'HPS', 'Hull Heal', 'Shield Heal', 'Max Heal', 'Crits', 'Heal Ticks', 
        'Crit Chance']

class DataWrapper():

    from OSCR.ui.styles import theme_font
    from OSCR.io import show_warning, store_json

    def analyze_log_callback(self, combat_id=None, path=None):
        """
        Wrapper function for retrieving and showing data. Callback of "Analyse" and "Refresh" button.
        
        Parameters:
        - :param combat_id: id of older combat (0 -> latest combat in the file; len(...) - 1 -> oldest combat)
        - :param path: path to combat log file
        """
        # initial run / click on the Analyze button
        if combat_id is None:
            if not path or not os.path.isfile(path):
                self.show_warning('Invalid Logfile', 'The Logfile you are trying to open does not exist.')
                return
            if path != self.settings['log_path']:
                self.settings['log_path'] = path
                self.store_json(self.settings, self.config['settings_path'])

            combats = self.get_data(combat=None, path=path)
            self.current_combats.clear()
            self.current_combats.addItems(combats)
            self.current_combats.setCurrentRow(0)
            self.current_combat_id = 0
            self.current_combat_path = path
            self.widgets['main_menu_buttons'][1].setDisabled(True)
            self.create_overview()

            analysis_thread = CustomThread(self.window, lambda: self.get_analysis_data(path))
            analysis_thread.start()
        # subsequent run / click on older combat
        elif isinstance(combat_id, int) and combat_id != self.current_combat_id:
            if combat_id == -1: return
            reversed_combat = self.current_combats.count() - 1 - combat_id
            self.get_data(reversed_combat)
            self.create_overview()
            self.current_combat_id = combat_id

            analysis_thread = CustomThread(self.window, 
                    lambda: self.get_analysis_data(self.current_combat_path, reversed_combat))
            analysis_thread.start()
        
        # reset tabber
        self.widgets['main_tabber'].setCurrentIndex(0)
        self.widgets['overview_tabber'].setCurrentIndex(0)

    def get_data(self, combat=None, path=None) -> Union[list, None]:
        """Interface between OSCRUI and OSCR. 
        Uses OSCR.parser class to fetch shallow combat data and stores it"""
        self.players = {}
        self.overview_data = [[],[],[],[],[]]

        # new log file
        if combat is None:
            self.parser = OSCR.parser()
            other_combats, _, _, dmg_data, dps_data, _, _ = self.parser.readCombatShallow(path)
            front_page_data = self.parser.createFrontPageTable()
            combats = [other_combats[j][1] for j in other_combats.keys()]
            combats.reverse()
        # same log file, old combat
        else:
            _, _, _, dmg_data, dps_data, _, _ = self.parser.readPreviousCombatShallow(combat)
            front_page_data = self.parser.createFrontPageTable()   

        # format Overview Table data
        for line in front_page_data[1:]:
            self.overview_data[0].append(line[1:])
            self.overview_data[2].append(line[0])
        self.overview_data[1] = front_page_data[0][1:]
        self.overview_data[3] = dps_data
        self.overview_data[4] = dmg_data

        if combat is None:
            return combats

    def get_analysis_data(self, path, id=None):
        """
        Starts new process using the multiprcessing module to retrieve full combat data.
        Populates the Analysis table. Don't use this in the main thread as it blocks execution.

        Parameters:
        - :param path: path to combat log file
        - :param id: id of older combat (0 -> oldest combat in the file; len(...) - 1 -> latest combat)
        """
        receiver, sender = Pipe()
        analysis_process = Process(target=analysis_parser, args=(path, sender, id))
        analysis_process.start()
        data = receiver.recv() # waits for the pipe to receive data from the process
        self.main_data = data
        """with open('new_data.json', 'w') as f:
            json.dump(data, f)"""
        self.populate_analysis()
        self.widgets['main_menu_buttons'][1].setDisabled(False)

    def format_data(self, el, integer=False) -> str:
        """
        rounds floats and ints to 2 decimals and sets 1000s seperators, ignores string values
        
        Parameters:
        - :param el: value to be formatted
        - :param integer: rounds numbers to zero decimal places when True (optional)
        """
        if isinstance(el, (int, float)):
            if not integer: return f'{el:,.2f}'
            else: return f'{el:,.0f}'
        elif isinstance(el, str):
            el = el.replace('â€“', '–')
            el = el.replace('Ãœ', 'Ü')
            el = el.replace('Ã¼', 'ü')
            el = el.replace('ÃŸ', 'ß')
            el = el.replace('Ã¶', 'ö')
            el = el.replace('Ã¤', 'ä')
            el = el.replace('â€˜', "'")
            return el
        else:
            return str(el)

    def populate_analysis(self):
        """
        Populates the Analysis' treeview table.
        """
        table = self.widgets['analysis_table_dout']
        model = TreeModel(DAMAGE_HEADER, self.theme_font('tree_table_header'),
                self.theme_font('tree_table'),
                self.theme_font('', self.theme['tree_table']['::item']['font']))
        model.populate_dout(self.main_data, 1)
        table.setModel(model)
        table.expand(model.index(0, 0))
        resize_tree_table(table)

        dtaken_table = self.widgets['analysis_table_dtaken']
        dtaken_model = TreeModel(DAMAGE_HEADER, self.theme_font('tree_table_header'),
                self.theme_font('tree_table'),
                self.theme_font('', self.theme['tree_table']['::item']['font']))
        dtaken_model.populate_in(self.main_data, 3)
        dtaken_table.setModel(dtaken_model)
        dtaken_table.expand(dtaken_model.index(0, 0))
        resize_tree_table(dtaken_table)

        hin_table = self.widgets['analysis_table_hin']
        hin_model = TreeModel(HEAL_HEADER, self.theme_font('tree_table_header'),
                self.theme_font('tree_table'),
                self.theme_font('', self.theme['tree_table']['::item']['font']))
        hin_model.populate_in(self.main_data, 6)
        hin_table.setModel(hin_model)
        hin_table.expand(hin_model.index(0, 0))
        resize_tree_table(hin_table)

        hout_table = self.widgets['analysis_table_hout']
        hout_model = TreeModel(HEAL_HEADER, self.theme_font('tree_table_header'),
                self.theme_font('tree_table'),
                self.theme_font('', self.theme['tree_table']['::item']['font']))
        hout_model.populate_dout(self.main_data, 4)
        hout_table.setModel(hout_model)
        hout_table.expand(hout_model.index(0, 0))
        resize_tree_table(hout_table)
        self.update_shown_columns_dmg()
        self.update_shown_columns_heal()

    def update_shown_columns_dmg(self):
        """
        Hides / shows columns of the dmg analysis table according to self.settings['dmg_columns']
        """
        dout_table = self.widgets['analysis_table_dout']
        dtaken_table = self.widgets['analysis_table_dtaken']
        for i, state in enumerate(self.settings['dmg_columns']):
            if state:
                dout_table.showColumn(i+1)
                dtaken_table.showColumn(i+1)
            else:
                dout_table.hideColumn(i+1)
                dtaken_table.hideColumn(i+1)
        self.store_json(self.settings, self.config['settings_path'])

    def update_shown_columns_heal(self):
        """
        Hides / shows columns of the heals analysis table according to self.settings['dmg_columns']
        """
        hout_table = self.widgets['analysis_table_hout']
        hin_table = self.widgets['analysis_table_hin']
        for i, state in enumerate(self.settings['heal_columns']):
            if state:
                hout_table.showColumn(i+1)
                hin_table.showColumn(i+1)
            else:
                hout_table.hideColumn(i+1)
                hin_table.hideColumn(i+1)
        self.store_json(self.settings, self.config['settings_path'])

class TableModel(QAbstractTableModel):
    def __init__(self, data, header, index, header_font:QFont, cell_font:QFont):
        super().__init__()
        self._data = data
        self._header = header
        self._index = index
        self._header_font = header_font
        self._cell_font = cell_font
    
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            current_col = index.column()
            cell = self._data[index.row()][current_col]
            if isinstance(cell, (float, int)) and current_col != 12:
                disp = f'{cell:,.2f}'
                if index.column() in (3, 5, 6, 7, 8, 10, 11):
                    disp += '%'
            else:
                disp = cell
            return disp
        
        if role == Qt.ItemDataRole.FontRole:
            return self._cell_font

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return AVCENTER + ARIGHT

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0]) # all columns must have the same length

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return TABLE_HEADER_CONVERSION[self._header[section]]

            if orientation == Qt.Orientation.Vertical:
                return self._index[section]

        if role == Qt.ItemDataRole.FontRole:
            return self._header_font

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if orientation == Qt.Orientation.Horizontal:
                return ACENTER

            if orientation == Qt.Orientation.Vertical:
                return AVCENTER + ARIGHT

class SortingProxy(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()

    def lessThan(self, left, right):
        l = self.sourceModel()._data[left.row()][left.column()]
        r = self.sourceModel()._data[right.row()][right.column()]
        return l < r

class TreeModel(QStandardItemModel):
    """
    Data Model for Analysis table
    """
    def __init__(self, header, header_font, name_font, cell_font):
        """
        Constructs a TreeModel with data accoring to the data table returned by OSCR.parser
        """
        self._header = header
        self._header_font = header_font
        self._name_font = name_font
        self._cell_font = cell_font
        super().__init__()
        self._root = self.invisibleRootItem()

    def headerData(self, section, orientation, role):
        try:
            if role == Qt.ItemDataRole.DisplayRole:
                return self._header[section]
            elif role == Qt.ItemDataRole.FontRole:
                return self._header_font
            elif role == Qt.ItemDataRole.TextAlignmentRole:
                return ACENTER
        except:
            sys.stdout.write(str((section, self._header)))

    def data(self, index, role):
        r = super().data(index, role)
        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(r, float):
                if index.column() in (8, 9, 10):
                    return f'{r:,.2f}%'
                return f'{r:,.2f}'
            return r
        elif role == Qt.ItemDataRole.FontRole:
            if index.column() == 0:
                return self._name_font
            else:
                return self._cell_font
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if index.column() != 0:
                return AVCENTER + ARIGHT

    def populate_in(self, data, index):
        """
        Converts and inserts the data into the model
        """
        player, player_row = std_item_generator(['Player']+['']*(len(self._header)-1), ())
        npc, npc_row = std_item_generator(['NPC']+['']*(len(self._header)-1), ())
        for player_name, stats in data.items():
            if self._is_passive(stats):
                continue
            current_entity, current_row = std_item_generator([player_name]+['']*(len(self._header)), (1,))
            if isinstance(stats[index], list):
                for ability in stats[index]:
                    _, ability_row = std_item_generator(ability[0], (1,))
                    current_entity.appendRow(ability_row)
                if stats[0]:
                    player.appendRow(current_row)
                else:
                    npc.appendRow(current_row)
        self._root.appendRow(player_row)
        self._root.appendRow(npc_row)

    def populate_dout(self, data, index):
        """
        Converts and inserts the data into the model
        """
        player, player_row = std_item_generator(['Player']+['']*(len(self._header)-1), ())
        npc, npc_row = std_item_generator(['NPC']+['']*(len(self._header)-1), ())
        for stats in data.values():
            if self._is_passive(stats):
                continue
            try:
                current_entity, current_row = std_item_generator(stats[index][0], (1,))
            except AttributeError:
                current_entity, current_row = std_item_generator([stats[1][0][0]]+['']*(len(self._header)), (1,))
            pet_sum_set = False
            pet_sum = None
            if isinstance(stats[index], list):
                for ability in stats[index][1:]:
                    if pet_sum_set or ability[0][0] != 'Pets (sum)':
                        self.insert_ability(ability, current_entity)
                    else:
                        pet_sum, pet_row = std_item_generator(ability[0], (1,))
                        current_entity.appendRow(pet_row)
                        pet_sum_set = True
                if stats[0]:
                    player.appendRow(current_row)
                else:
                    npc.appendRow(current_row)
            if index == 1 and isinstance(stats[2], list):
                for pet_ability in stats[2]:
                    self.insert_ability(pet_ability, pet_sum, name_index=0)   
        self._root.appendRow(player_row)
        self._root.appendRow(npc_row)

    def insert_ability(self, ability:list, parent:StandardItem, name_index:int=1, sub_index:int=0):
        """
        Recursively adds an ability and its sub-abilites to parent
        """
        global_, global_row  = std_item_generator(ability[0], (name_index,)) #self._to_standard_item(filtered_ability(ability[0], (1,)))
        for line in ability[1:]:
            if isinstance(line[0], list): #len(line) > 0 and 
                if len(ability) == 2:
                    #lili = line[0][1].replace(re_sub('[0-9]+(?!\))$', '', ability[0][1]).strip(), '').strip()
                    global_.set_val(f'{line[0][1]}')
                    if isinstance(line[1][0], list):
                        for child_line in line[1:]:
                            self.insert_ability(child_line, global_, name_index, sub_index)
                    else:
                        for child_line in line[1:]:
                            global_.appendRow(std_item_generator(child_line, (sub_index,))[1])
                else:
                # if len(ability) == 2 and isinstance(line[1][0], list):
                #     if line[0][0].startswith('C['):
                #         global_.set_val(f'{global_.get_val()} {get_entity_num(line[0][0])}')
                #     elif line[0][0].startswith('P['):
                #         global_.set_val(clean_player_id(line[0][0]))
                #     for child_line in line[1:]:
                #         self.insert_ability(child_line, global_)
                # elif len(ability) == 2 and isinstance(line[1][0], str):
                #     global_.set_val(f'{line[0][0]} {get_entity_num(ability[0][0])}')
                #     for child_line in line[1:]:
                #         global_.appendRow(self._to_standard_item(filtered_ability(child_line, (0,))))
                # else:
                #     self.insert_ability(line, global_)
                    self.insert_ability(line, global_, name_index, sub_index)
            elif isinstance(line[0], str): # len(line) > 0 and 
                global_.appendRow(std_item_generator(line, (sub_index,))[1])
                #global_.appendRow(self._to_standard_item(filtered_ability(line, (0,))))
        parent.appendRow(global_row)


    def _to_standard_item(self, it) -> tuple[StandardItem, ...]:
        """
        Converts each element in iterable to StandardItem and returns them as tuple 
        """
        return tuple(map(StandardItem, it))

    def _is_passive(self, ar:list):
        """
        Determines whether entity engaged in combat
        """
        if len(ar[1]) < 2:
            # Entity did not deal any damage
            return True
        if len(ar[4]) == 0:
            return True
        return False
