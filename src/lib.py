from re import sub as re_sub

from PyQt6.QtCore import QThread, pyqtSignal

from src import OSCR

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