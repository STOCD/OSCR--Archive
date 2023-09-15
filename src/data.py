from src import OSCR
from PyQt6.QtWidgets import QMessageBox
from operator import itemgetter
import os
import json
import numpy as np

class DataWrapper():

    from src.io import show_warning

    

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
        for key in data.keys():
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
                self.players[key] = (player_index, player_abilities)
        
        self.misc_combat_data = data2
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