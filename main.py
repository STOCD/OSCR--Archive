import sys
import os
from src.app import OpenSourceCombatlogReader

class Launcher():

    version = '2023.9a110'

    theme = {
        'app': {
            'bg': '#1a1a1a',
            'oscr': '#c82934',
            'margin': 8,
            'font': ('Overpass', 15, 'normal'),
            'font-fallback': ('Yu Gothic UI', 'Nirmala UI', 'Microsoft YaHei UI', 'sans-serif')
        },
        'defaults': {
            'bg': '#1a1a1a',
            'oscr': '#c82934',
            'font': ('Overpass', 15, 'normal'),
            'fg': '#eeeeee',
        },
        'frame': {
            'background': '#1a1a1a',
            'margin': 0,
            'padding': 0
        },
        'medium_frame': {
            'background': '#242424',
            'margin': 0,
            'padding': 0
        },
        'label': {
            'font': ('Overpass', 15, 'normal'),
            'color': '#eeeeee'
        },
        'menu_button': {
            'background': 'rgba(0,0,0,0)',
            'color': '#eeeeee',
            'text-decoration': 'none',
            'border': 'none',
            'margin-left': 10,
            'margin-top': 5,
            'margin-bottom': 4,
            'margin-right': 10,
            'padding': 0,
            'font': ('Overpass', 20, 'bold'),
            'hover': {
                'text-decoration': 'underline',
                'color': '#eeeeee'
            }
        },
        'small_button': {
            'background': 'rgba(0,0,0,0)',
            'border': '2px solid #a0a0a0',
            'border-radius': 3
        }
    }

    def __init__(self):
        try:
            self.base_path = sys._MEIPASS
        except Exception:
            self.base_path = os.path.abspath(os.path.dirname(__file__))
        sys.path.append(self.base_path)
        self.args = {}

    def launch(self):
        sys.exit(OpenSourceCombatlogReader(self.version, self.theme, self.args, self.base_path).run())

if __name__ == '__main__':
    Launcher().launch()