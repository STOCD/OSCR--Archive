from PyQt6.QtWidgets import QApplication, QWidget, QFrame, QLabel, QSizePolicy, QPushButton, QScrollArea
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont, QFontDatabase
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtSvg import QSvgRenderer
from src.ui.widgets import BannerLabel, WidgetBuilder
import copy

class OscrGui(WidgetBuilder):

    from src.ui.styles import get_style, get_css, get_style_class
    from src.io import get_asset_path

    def __init__(self, path) -> None:
        """
        This class is not inteded to be instantiated.
        """
        return

    def create_main_window(self, argv=[]):
        app = QApplication(argv)
        window = QWidget()
        icon_path = self.get_asset_path('oscr_icon_small.png')
        window.setWindowIcon(QIcon(icon_path))
        window.setWindowTitle('Open Source Combatlog Reader')
        window.setGeometry(*self.get_relative_geometry(app))
        window.showMaximized()
        return app, window

    def setup_main_layout(self):
        layout =  QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        bg_frame = QFrame(self.window)
        bg_frame.setStyleSheet(self.get_css({'background': self.theme['app']['oscr']}))
        layout.addWidget(bg_frame)
        self.window.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        lbl = BannerLabel(self.get_asset_path('oscrbanner-slim-dark-label.png'), bg_frame)
        main_layout.addWidget(lbl)
        menu_frame = self.create_frame(bg_frame, 'frame', {'background':'#c82934'})
        menu_frame.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        menu_frame.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(menu_frame)
        main_frame = self.create_frame(bg_frame, 'frame', {'margin':'0px 8px 8px 8px'})
        main_layout.addWidget(main_frame)
        bg_frame.setLayout(main_layout)

        menu_button_style = {
            'Overview': {'callback':lambda: print('Overview Button Pressed'), 'style':{'margin-left':15}},
            'Analysis': {'callback':lambda: print('Analysis Button Pressed')},
            'League Standings': {'callback':lambda: print('League Button Pressed')},
            'Settings': {'callback':lambda: print('Settings Button Pressed')},
        }
        buttons = self.create_button_series(menu_frame, menu_button_style, 'menu_button', seperator='•')
        menu_frame.setLayout(buttons)

        content_layout = QGridLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        left = self.create_frame(main_frame, 'medium_frame', {'background': '#3c3c3c'})
        left.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        content_layout.addWidget(left, 0, 0)
        center = self.create_frame(main_frame, 'frame', {'background': '#222222'})
        center.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        content_layout.addWidget(center, 0, 2)

        lb = self.create_label('placeholder label with long text', 'label', left)
        ll = QVBoxLayout()
        ll.addWidget(lb, alignment=Qt.AlignmentFlag.AlignTop)
        left.setLayout(ll)
        
        main_frame.setLayout(content_layout)



    def get_relative_geometry(self, app:QApplication, pos=(0.1, 0.1), size=(0.8, 0.8)):
        """
        Returns tuple containing x and y positions as well as width and height of a window
        in given order, relative to the current screen. All values are given in pixels.

        Parameters:
        - :param pos: (tuple of two floats) -> relative position of the top left corner
        - :param size: (tuple of two floats) -> relative size of the window
        """
        rel_x, rel_y = pos
        rel_size_x, rel_size_y = size
        rect = app.primaryScreen().availableGeometry()
        _, _, width, height = rect.getRect()
        pos_x = rel_x * width
        pos_y = rel_y * height
        width = rel_size_x * width
        height = rel_size_y * height
        return (pos_x, pos_y, width, height)