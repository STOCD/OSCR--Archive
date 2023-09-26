from multiprocessing import Lock
import os
import json
import copy

from src.ui.core import OscrGui


class OpenSourceCombatlogReader(OscrGui):

    from src.io import load_icon, format_path, fetch_json, store_json

    app_dir = None

    config = {} # see main.py for contents

    settings = {} # see main.py for defaults

    # stores widgets that need to be accessed from outside their creating function
    widgets = {
        'main_menu_buttons': [],
        'overview_menu_buttons': [],
        'main_tabber': None,
        'overview_tabber': None,
        'main_tab_frames': [],
        'overview_tab_frames': [],
        'overview_graphs': [],
        'analysis_table': None,
    }
    
    def __init__(self, version, theme, args, path, config) -> None:
        """
        Creates new Instance of OSCR.

        Parameters:
        - :param version: version of the app
        - :param theme: dict -> default theme
        - :param args: command line arguments
        - :param path: absolute path to main.py file
        - :param config: app configuration (!= settings these are not changed by the user)
        """
        self.version = version
        self.theme = theme
        self.args = args
        self.app_dir = path
        self.config = config
        self.app, self.window = self.create_main_window()
        self.init_config()
        self.init_settings()
        self.cache_assets()
        self.setup_main_layout()

    def run(self) -> int:
        """
        Runs the event loop.

        :return: exit code of event loop
        """
        return self.app.exec()

    def cache_assets(self):
        """
        Caches assets like icon images
        """
        self.icons = {}
        self.icons['expand-left'] = self.load_icon('expand-left.svg')
        self.icons['collapse-left'] = self.load_icon('collapse-left.svg')
        self.icons['expand-right'] = self.load_icon('expand-right.svg')
        self.icons['collapse-right'] = self.load_icon('collapse-right.svg')
        self.icons['refresh'] = self.load_icon('refresh-cw.svg')

    def init_settings(self):
        """
        Prepares settings. Loads stored settings. Saves current settings for next startup.
        """
        self.settings['log_path'] = self.format_path(self.app_dir)
        try:
            stored_settings = self.fetch_json(self.config['settings_path'])
            self.settings = copy.copy(self.config['default_settings'])
            self.settings.update(stored_settings)
        except (FileNotFoundError, json.JSONDecodeError):
            self.settings = copy.copy(self.config['default_settings'])
        finally:
            self.store_json(self.settings, self.config['settings_path'])
        

    def init_config(self):
        """
        Prepares config.
        """
        self.config['default_settings']['log_path'] = self.format_path(
                self.config['default_settings']['log_path'])
        _, _, screen_width, _ = self.app.primaryScreen().availableGeometry().getRect()
        self.config['sidebar_item_width'] = int(self.theme['s.c']['sidebar_item_width'] * screen_width)
        style_path = rf"{self.app_dir}/{self.config['plot_stylesheet_path']}"
        self.config['plot_stylesheet_path'] = os.path.normpath(os.path.abspath(style_path))
        settings_path = rf"{self.app_dir}/{self.config['settings_path']}"
        self.config['settings_path'] = os.path.normpath(os.path.abspath(settings_path))
        self.config['parser1_lock'] = Lock()
        self.current_combat_id = -1
        self.current_combat_path = ''