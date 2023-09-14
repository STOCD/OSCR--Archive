from src.ui.core import OscrGui


class OpenSourceCombatlogReader(OscrGui):

    from src.io import load_icon, format_path

    app_dir = None

    settings = {
        'sidebar_item_width': 0
    }
    
    def __init__(self, version, theme, args, path, config) -> None:
        self.version = version
        self.theme = theme
        self.args = args
        self.app_dir = path
        config.update(self.settings)
        self.settings = config
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

    def init_settings(self):
        """
        Prepares settings.
        """
        _, _, screen_width, _ = self.app.primaryScreen().availableGeometry().getRect()
        self.settings['sidebar_item_width'] = 0.15 * screen_width
        self.settings['base_path'] = self.format_path(self.settings['base_path'])

    def attach_callbacks(self):
        """
        Attaches callbacks defined in this class to widgets
        """
        