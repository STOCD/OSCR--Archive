from re import sub as re_sub

from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QStandardItem

import OSCR

def clean_player_id(id:str) -> str:
    """
    cleans player id and returns handle
    """
    return id[id.find(' ')+1:-1]

def clean_entity_id(id:str) -> str:
    """
    cleans entity id and returns it
    """
    return re_sub(r'C\[([0-9]+) +?([a-zA-Z_0-9]+)\]', r'\2 \1', id).replace('_', ' ')

def get_entity_num(id:str) -> int:
    """
    gets entity number from entity id
    """
    if not id.startswith('C['):
        return -1
    try:
        return int(re_sub(r'C\[([0-9]+) +?([a-zA-Z_0-9]+)\]', r'\1', id))
    except ValueError:
        return int(re_sub(r'C\[([0-9]+) +?([a-zA-Z_0-9]+)\]_WCB', r'\1', id))
    except TypeError:
        return -1

def set_variable(var_to_be_set, index, value):
    """
    Assigns value at index to variable
    """
    var_to_be_set[index] = value

def filtered_ability(list: list, index):
    """
    Generator that returns all items of list except the item in index.
    Also cleans entity ids and ability names. The first item to be returned must be of type str.

    Parameters:
    - :param list: list -> original list
    - :param index: iterable containing one or more indexes to be excluded from return

    :return: Generator 
    """
    for ix, item in enumerate(list):
        if ix not in index:
            if ix == 0 or ix == 1:
                try:
                    if item.startswith('C['):
                        yield clean_entity_id(item)
                    elif item.startswith('P['):
                        yield clean_player_id(item)
                    else:
                        yield compensate_text(item)
                except AttributeError:
                    raise TypeError(f'The first table column must contain a str, not {type(item).__name__}')
            else:
                yield item

def compensate_text(text:str) -> str:
    """
    Unescapes various characters not correctly represented in combatlog files

    Parameters:
    - :param text: str -> text to be cleaned

    :return: cleaned text
    """
    text = text.replace('â€“', '–')
    text = text.replace('Ãœ', 'Ü')
    text = text.replace('Ã¼', 'ü')
    text = text.replace('ÃŸ', 'ß')
    text = text.replace('Ã¶', 'ö')
    text = text.replace('Ã¤', 'ä')
    text = text.replace('â€˜', "'")
    return text

def resize_tree_table(tree):
    """
    Resizes the columns of the given tree table to fit its contents

    Parameters:
    - :param tree: QTreeView -> tree to be resized
    """
    for col in range(tree.header().count()):
        width = max(tree.sizeHintForColumn(col), tree.header().sectionSizeHint(col)) + 5
        tree.header().resizeSection(col, width)

def analysis_parser(path, pipe, id=None):
    """
    Retrieves combat analysis data from parser. Used in different process.

    Parameters:
    - :param path: path of the combat log to be analyzed
    - :param pipe: pipe to transmit results back through
    - :param id: older combat id (optional)
    """
    parser = OSCR.parser()
    if id is None:
        parser.readCombatShallow(path)
        uiD, dmgI, healI, uiID, _, _, _, _, _, npcdmg, npcdps = parser.readCombatFull(path)
    elif isinstance(id, int):
        parser.readCombatShallow(path)
        uiD, dmgI, healI, uiID, _, _, _, _, _, npcdmg, npcdps = parser.readPreviousCombatFull(id)
    pipe.send(uiD)


class CustomThread(QThread):
    """
    Subclass of QThread able to execute an arbitrary function in a seperate thread.
    """
    result = pyqtSignal(tuple)

    def __init__(self, parent, func) -> None:
        self._func = func
        super().__init__(parent)

    def run(self):
        r = self._func()
        self.result.emit((r,))

class StandardItem(QStandardItem):
    """
    Standard Item supporting str, int and float data types
    """
    def __init__(self, value):
        if not isinstance(value, (str, int, float)):
            raise TypeError(f'StandardItem only supports str, int or float; not {type(value).__name__}')
        self._val = value
        super().__init__()

    def data(self, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._val
        return super().data(role)

    def set_val(self, val):
        if not isinstance(val, (str, int, float)):
            raise TypeError(f'StandardItem only supports str, int or float; not {type(val).__name__}')
        self._val = val
    
    def get_val(self):
        return self._val

def std_item_generator(item_list:list, exclude_index:tuple):

    def _gen(ar, index, first_item, first_index):
        yield first_item
        for ix, item in enumerate(ar):
            if ix in index or ix == first_index:
                continue
            yield StandardItem(item)

    i = 0 if not 0 in exclude_index else 1
    if item_list[i].startswith('P['):
        first = StandardItem(clean_player_id(item_list[i]))
    elif item_list[i].startswith('C['):
        first = StandardItem(clean_entity_id(item_list[i]))
    else:
        first = StandardItem(compensate_text(item_list[i]))

    return first, _gen(item_list, exclude_index, first, i)

class StdItemGenerator():
    def __init__(self, ar:list, index:tuple):
        self._i = 0 if not 0 in index else 1
        if ar[self._i][0] == 'P':
            self._first = StandardItem(clean_player_id(ar[self._i]))
        elif ar[self._i][0] == 'C':
            self._first = StandardItem(clean_entity_id(ar[self._i]))
        else:
            self._first = StandardItem(compensate_text(ar[self._i]))

    def _gen(self, ar, index):
        yield self._first
        for ix, item in enumerate(ar):
            if ix in index or ix == self._i:
                continue
            yield StandardItem(item)
