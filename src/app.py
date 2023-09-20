from src.ui.core import OscrGui
import os


class OpenSourceCombatlogReader(OscrGui):

    from src.io import load_icon, format_path

    app_dir = None

    settings = {
        'sidebar_item_width': 0,
        'plot_stylesheet_path': r'/src/ui/oscr_default.mplstyle',
    }

    widgets = {
        'main_menu_buttons': [],
        'second_menu_buttons': [],
        'main_tab_frames': [],
        'overview_tab_frames': [],
        'overview_graphs': [],
        'analysis_table': None,
    }
    
    def __init__(self, version, theme, args, path, config) -> None:
        self.version = version
        self.theme = theme
        self.args = args
        self.app_dir = path
        #config.update(self.settings)
        #self.settings = config
        self.app, self.window = self.create_main_window()
        self.init_settings()
        self.cache_assets()
        self.setup_main_layout()
        self.attach_callbacks()

    def run(self):
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
        Prepares settings.
        """
        _, _, screen_width, _ = self.app.primaryScreen().availableGeometry().getRect()
        self.settings['sidebar_item_width'] = int(self.theme['s.c']['sidebar_item_width'] * screen_width)
        self.settings['base_path'] = self.format_path(self.app_dir)
        style_path = rf"{self.app_dir}/{self.settings['plot_stylesheet_path']}"
        self.settings['plot_stylesheet_path'] = os.path.normpath(os.path.abspath(style_path))

    def attach_callbacks(self):
        """
        Attaches callbacks defined in this class to widgets
        """
