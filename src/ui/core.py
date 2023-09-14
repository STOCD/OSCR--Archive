from PyQt6.QtWidgets import QApplication, QWidget, QSizePolicy, QLineEdit, QFrame, QListWidget
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QAbstractItemView
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont, QFontDatabase
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtSvg import QSvgRenderer
from src.ui.widgets import BannerLabel, WidgetBuilder, FlipButton
from src.ui.widgets import SMAXMAX, SMAXMIN, SMINMAX, SMINMIN, ALEFT, ARIGHT, ATOP
import os
import copy

class OscrGui(WidgetBuilder):

    from src.ui.styles import get_style, get_css, get_style_class, create_style_sheet
    from src.io import get_asset_path, browse_path

    def __init__(self, path) -> None:
        """
        This class is not inteded to be instantiated.
        """
        return

    def create_main_window(self, argv=[]):
        app = QApplication(argv)
        app.setStyleSheet(self.create_style_sheet(self.theme['app']['style']))
        window = QWidget()
        icon_path = self.get_asset_path('oscr_icon_small.png')
        window.setWindowIcon(QIcon(icon_path))
        window.setWindowTitle('Open Source Combatlog Reader')
        window.setGeometry(*self.get_relative_geometry(app))
        window.showMaximized()
        return app, window

    def setup_main_layout(self):
        layout, main_frame = self.create_master_layout(self.window)
        self.window.setLayout(layout)

        content_layout = QGridLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        left = self.create_frame(main_frame, 'medium_frame')
        left.setSizePolicy(SMAXMIN)
        content_layout.addWidget(left, 0, 0)

        right = self.create_frame(main_frame, 'frame', 
                {'border-left-style': 'solid', 'border-left-width': '@sep', 'border-left-color': '@oscr' })
        right.setSizePolicy(SMINMIN)
        right.hide()
        content_layout.addWidget(right, 0, 4)

        icon_size = self.theme['s.c']['button_icon_size']
        left_flip_config = {
            'icon_r': self.icons['collapse-left'], 'func_r': left.hide,
            'icon_l': self.icons['expand-left'], 'func_l': left.show
        }
        right_flip_config = {
            'icon_r': self.icons['expand-right'], 'func_r': right.show,
            'icon_l': self.icons['collapse-right'], 'func_l': right.hide
        }
        for col, config in ((1, left_flip_config), (3, right_flip_config)):
            flip_button = FlipButton('', '', main_frame)
            flip_button.configure(config)
            flip_button.setIconSize(QSize(icon_size, icon_size))
            flip_button.setStyleSheet(self.get_style_class('QPushButton', 'small_button'))
            flip_button.setSizePolicy(SMAXMAX)
            content_layout.addWidget(flip_button, 0, col, alignment=ATOP)

        center = self.create_frame(main_frame, 'frame')
        center.setSizePolicy(SMINMIN)
        content_layout.addWidget(center, 0, 2)

        main_frame.setLayout(content_layout)
        self.setup_left_sidebar(left)

    def setup_left_sidebar(self, frame:QFrame):
        left_layout = QVBoxLayout()
        m = self.theme['app']['margin']
        left_layout.setContentsMargins(m, m, m, m)
        left_layout.setSpacing(0)
        left_layout.setAlignment(ATOP)

        head = self.create_label('STO Combatlog:', 'label', frame)
        left_layout.addWidget(head, alignment=ALEFT)

        entry = QLineEdit(self.settings['base_path'], frame)
        entry.setFixedWidth(self.settings['sidebar_item_width'])
        entry.setStyleSheet(self.get_style_class('QLineEdit', 'entry'))
        entry.setSizePolicy(SMAXMAX)
        left_layout.addWidget(entry)
        
        button_frame = self.create_frame(frame, 'medium_frame')
        button_frame.setSizePolicy(SMINMAX)
        entry_button_config = {
            'default': {'margin-bottom': 15},
            'Browse ...': {'callback': lambda: self.browse_log(entry), 'align': ALEFT},
            'Analyze': {'callback': lambda: print('analyze'), 'align': ARIGHT}
        }
        entry_buttons = self.create_button_series(button_frame, entry_button_config, 'button')
        button_frame.setLayout(entry_buttons)
        left_layout.addWidget(button_frame)

        background_frame = self.create_frame(frame, 'light_frame', {'border-radius': 2})
        background_frame.setSizePolicy(SMAXMIN)
        background_layout = QVBoxLayout()
        background_layout.setContentsMargins(0, 0, 0, 0)
        background_frame.setLayout(background_layout)
        self.current_combats = QListWidget(background_frame)
        self.current_combats.setStyleSheet(self.get_style_class('QListWidget', 'listbox'))
        self.current_combats.setFont(self.theme_font('listbox'))
        self.current_combats.insertItems(0, ['Infected Space (Elite) Combat ddddddxxxxddddddddddddddxxxxdddddd']*25)
        self.current_combats.setSizePolicy(SMAXMIN)
        self.current_combats.setFixedWidth(self.settings['sidebar_item_width'])
        background_layout.addWidget(self.current_combats)
        left_layout.addWidget(background_frame, stretch=1)

        frame.setLayout(left_layout)



    def create_master_layout(self, parent):
        """
        Creates and returns the master layout for an OSCR window.

        Parameters:
        - :param parent: parent to the layout, usually a window

        :return: populated QVBoxlayout and content frame QFrame
        """
        layout =  QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        bg_frame = self.create_frame(parent, 'frame', {'background': '@oscr'})
        bg_frame.setSizePolicy(SMINMIN)
        layout.addWidget(bg_frame)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        lbl = BannerLabel(self.get_asset_path('oscrbanner-slim-dark-label.png'), bg_frame)
        
        main_layout.addWidget(lbl)

        menu_frame = self.create_frame(bg_frame, 'frame', {'background':'#c82934'})
        menu_frame.setSizePolicy(SMAXMAX)
        menu_frame.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(menu_frame)
        menu_button_style = {
            'Overview': {'callback':lambda: print('Overview Button Pressed'), 'style':{'margin-left':15}},
            'Analysis': {'callback':lambda: print('Analysis Button Pressed')},
            'League Standings': {'callback':lambda: print('League Button Pressed')},
            'Settings': {'callback':lambda: print('Settings Button Pressed')},
        }
        buttons = self.create_button_series(menu_frame, menu_button_style, 'menu_button', seperator='•')
        menu_frame.setLayout(buttons)

        main_frame = self.create_frame(bg_frame, 'frame', {'margin':'0px 8px 8px 8px'})
        main_frame.setSizePolicy(SMINMIN)
        main_layout.addWidget(main_frame)
        bg_frame.setLayout(main_layout)

        return layout, main_frame


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

    def browse_log(self, entry:QLineEdit):
        """
        Callback for browse button.
        """
        current_path = entry.text()
        if current_path != '':
            path = self.browse_path(os.path.dirname(current_path), 'Logfile (*.log);;Any File (*.*)')
            if path != '':
                entry.setText(path)