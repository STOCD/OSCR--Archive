from re import sub as re_sub
from PyQt6.QtCore import QThread, pyqtSignal
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

def filtered_ability(list: list, index):
    """
    Generator that returns all items of list except the item in index.
    Also cleans entity ids and ability names.
    """
    for ix, item in enumerate(list):
        if ix not in index:
            if ix == 0 or ix == 1:
                try:
                    if item.startswith('C['):
                        yield clean_entity_id(item)
                    else:
                        yield compensate_text(item)
                except AttributeError:
                    raise TypeError(f'The first table column must contain a str, not {type(item).__name__}')
            else:
                yield item

def compensate_text(text:str) -> str:
    """
    Unescapes various characters not correctly represented in combatlog files
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
    """
    for col in range(tree.header().count()):
        width = max(tree.sizeHintForColumn(col), tree.header().sectionSizeHint(col)) + 5
        tree.header().resizeSection(col, width)


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
        self.result.emit(tuple([r]))