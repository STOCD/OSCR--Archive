from src import OSCR
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QAbstractTableModel, Qt, QSortFilterProxyModel
from operator import itemgetter
import os
import json
import numpy as np

HEADER_CONVERSION = {
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
    '% healed': 'Heals Share', # %
    'deaths': 'Deaths'
}

class DataWrapper():

    from src.io import show_warning

    table_header_conversion = {

    }

    def get_data(self, combat=None, path=None):
        """Interface between OSCRUI and OSCR. 
        Uses OSCR.parser class to fetch combat data and stores it"""

        self.players = {}
        self.overview_data = [[],[],[]]

        # initial run / click on the Analyze button
        if combat is None:
            self.parser = OSCR.parser()
            self.parser.readCombatwithUITables(path)
            data, *data2 = self.parser.readPreviousCombatwithUITables(0)
            combats = [self.parser.otherCombats[j][1] 
                    for j in self.parser.otherCombats.keys()]
            combats.reverse()

        # subsequent run / click on older combat
        else:
            data, *data2 = self.parser.readPreviousCombatwithUITables(combat)
        raw_front_data = self.parser.createFrontPageTable()        

        # format Overview Table data
        for line in raw_front_data[1:]:
            self.overview_data[0].append(line[1:])
            self.overview_data[2].append(line[0])
        self.overview_data[1] = raw_front_data[0][1:]
        # format Combat Analysis data
        """for key in data.keys():
            if key[0] == 'P':
                abilities = []
                for ability in data[key][1]:
                    if ability[0][0] != 'Pets (sum)':
                        abilities.append([ability[0][0], *ability[0][2:]])
                for pet in data[key][2]:
                    abilities.append([f'{pet[0][0]} (Pet)', *pet[0][2:]])
                abilities = sorted(abilities, 
                        key=itemgetter(2), reverse=True)
                player_index = [self.format_data(line[0]) for line in abilities]
                player_abilities = [line[1:] for line in abilities]
                #self.format_analysis_table(player_abilities)
                self.players[key] = (player_index, player_abilities)"""
        
        self.misc_combat_data = data2
        print(self.overview_data)
        if combat is None:
            return combats
        # update map name and difficulty
        """with open('data.json', 'w') as f:
            json.dump(self.misc_combat_data[6][list(self.misc_combat_data[6].keys())[0]], f)"""
        """with open('data.json', 'w') as f:
            json.dump(data, f)
        with open('data1.json', 'w') as fil:
            json.dump(self.misc_combat_data[6], fil)
        with open('data2.json', 'w') as fil:
            json.dump(self.misc_combat_data[7], fil)"""

    def format_data(self, el, integer=False):
        """rounds floats and ints to 2 decimals and sets 1000s seperators, 
        ignores string values"""
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

class TableModel(QAbstractTableModel):
    def __init__(self, data, header, index, header_font:QFont, cell_font:QFont):
        super().__init__()
        self._data = data
        self._header = header
        self._index = index
        self._header_font = header_font
        self._cell_font = cell_font
    
    def data(self, index, role):
        # format data here if necessary
        if role == Qt.ItemDataRole.DisplayRole:
            current_col = index.column()
            cell = self._data[index.row()][current_col]
            if isinstance(cell, (float, int)) and current_col != 11:
                disp = f'{cell:,.2f}'
                if index.column() in (3, 5, 6, 7, 8, 10):
                    disp += '%'
            else:
                disp = cell
            return disp
        
        if role == Qt.ItemDataRole.FontRole:
            return self._cell_font

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0]) # all columns must have the same length

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return HEADER_CONVERSION[self._header[section]]

            if orientation == Qt.Orientation.Vertical:
                return self._index[section]

        if role == Qt.ItemDataRole.FontRole:
            return self._header_font

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if orientation == Qt.Orientation.Horizontal:
                return Qt.AlignmentFlag.AlignCenter

            if orientation == Qt.Orientation.Vertical:
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

class SortingProxy(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()

    def lessThan(self, left, right):
        l = self.sourceModel()._data[left.row()][left.column()]
        r = self.sourceModel()._data[right.row()][right.column()]
        return l < r