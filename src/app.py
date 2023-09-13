from src.ui.core import OscrGui


class OpenSourceCombatlogReader(OscrGui):

    from src.io import load_icon

    app_dir = None
    
    def __init__(self, version, theme, args, path) -> None:
        self.version = version
        self.theme = theme
        self.args = args
        self.app_dir = path
        self.app, self.window = self.create_main_window()
        self.cache_assets()
        self.setup_main_layout()

    def run(self):
        return self.app.exec()

    def cache_assets(self):
        """
        Caches assets like icon images
        """
        self.icons = {}
        self.icons['expand'] = self.load_icon('expand-icon.png', 24)
        self.icons['collapse'] = self.load_icon('collapse-icon.png', 24)