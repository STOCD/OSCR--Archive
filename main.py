import sys
import os
from src.app import OpenSourceCombatlogReader

class Launcher():

    version = '2023.9a110'

    theme = {
        'app': {
            'bg': '#1a1a1a',
            'fg': '#eeeeee',
            'oscr': '#c82934',
            'margin': 10,
            'font': ('Overpass', 15, 'normal'),
            'font-fallback': ('Yu Gothic UI', 'Nirmala UI', 'Microsoft YaHei UI', 'sans-serif'),
            'style': {
                'QScrollBar': {
                    'background': 'none',
                    'border': 'none',
                    'border-radius': 0,
                    'margin': 0
                },
                'QScrollBar:vertical': {
                    'width': 10,    
                },
                'QScrollBar:horizontal': {
                    'height': 10,    
                },
                'QScrollBar::add-page, QScrollBar::sub-page': {
                    'background': 'none'
                },
                'QScrollBar::handle': {
                    'background': 'red',
                    'background-color': '#101010',
                    'border-radius': 5,
                    'border': 'none'
                },
                'QScrollBar::add-line, QScrollBar::sub-line': {
                    'height': 0
                }
            }
        },
        'defaults': {
            'bg': '#1a1a1a',
            'mbg': '#242424',
            'lbg': '#404040',
            'oscr': '#c82934',
            'font': ('Overpass', 15, 'normal'),
            'fg': '#eeeeee',
            'mfg': '#bbbbbb',
            'bc': '#888888',
            'sep': 2,
            'margin': 10
        },
        'frame': {
            'background': '@bg',
            'margin': 0,
            'padding': 0
        },
        'medium_frame': {
            'background': '@mbg',
            'margin': 0,
            'padding': 0
        },
        'light_frame': {
            'background': '@lbg',
            'margin': 0,
            'padding': 0
        },
        'label': {
            'color': '@fg',
            'margin': (3, 0, 3, 0),
            'padding-left': 0,
            'qproperty-indent': '0'
        },
        'button': {
            'background': 'none',
            'color': '@fg',
            'text-decoration': 'none',
            'border': 'none', #'1px solid #606060',
            'border-radius': 2,
            'margin': (3, 10, 3, 10),
            'padding': (2, 5, 0, 5),
            'font': ('Overpass', 15, 'medium'),
            ':hover': {
                'color': '@fg',
                'border': '1px solid #c82934'
            }
        },
        'menu_button': {
            'background': 'none',
            'color': '@fg',
            'text-decoration': 'none',
            'border': 'none',
            'margin-left': 10,
            'margin-top': 6,
            'margin-bottom': 4,
            'margin-right': 10,
            'padding': 0,
            'font': ('Overpass', 20, 'bold'),
            ':hover': {
                'text-decoration': 'underline',
                'color': '@fg'
            }
        },
        'small_button': {
            'background': 'none',
            'border': 'none',
            'border-radius': 3,
            'margin-left': 4,
            'margin-top': 4,
            'margin-bottom': 1,
            'margin-right': 2,
            'padding': (2, 0, 2, 0),
            ':hover': {
                'background': 'rgba(136,136,136,.2)'
            }
        },
        'icon_button': {
            'background': 'none',
            'border': '1px solid #888888',
            'border-radius': 3,
            'margin-left': 1,
            'margin-top': 1,
            'margin-bottom': 1,
            'margin-right': 1,
            'padding': (2, 0, 2, 0),
            ':hover': {
                'border-color': '@oscr'
            }
        },
        'entry': {
            'background': '@lbg',
            'color': '@fg',
            'border': '1px solid #888888',
            'border-radius': 2,
            'font': ('Overpass', 12, 'normal'),
            ':focus': {
                'border-color': '@oscr'
            }
        },
        'listbox': {
            'background': '@lbg',
            'color': '@fg',
            'border': '1px solid #888888',
            'border-radius': 2,
            'font': ('Overpass', 10, 'normal'),
            'outline': 0,
            '::item': {
                'border': '1px solid #404040'
            },
            '::item:selected': {
                'background': 'none',
                'border': '1px solid #c82934',
                'border-radius': 2,
            },
            '::item:selected:!active': {
                'color':'@fg'
            },
            '::item:hover': {
                'background': '#20c82934',
            },
        },
        'tabber': {
            'background': 'none',
            'border': 'none',
            'margin': 0,
            'padding': 0,
            '::pane': {
                'border': 'none'
            }
        },
        'tabber_tab': {
            '::tab': {
                'height': 0,
                'width': 0
            }
        },
        's.c': {
            'button_icon_size': 24
        }
    }

    config = {
        'base_path': ''
    }

    def __init__(self):
        try:
            self.base_path = sys._MEIPASS
        except Exception:
            self.base_path = os.path.abspath(os.path.dirname(__file__))
        sys.path.append(self.base_path)
        self.config['base_path'] = self.base_path
        self.args = {}

    def launch(self):
        c = OpenSourceCombatlogReader(self.version, self.theme, self.args, self.base_path, self.config).run()
        sys.exit(c)

if __name__ == '__main__':
    Launcher().launch()