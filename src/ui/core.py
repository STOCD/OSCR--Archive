from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QFrame, QListWidget, QTabWidget
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QAbstractItemView
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont, QFontDatabase
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtSvg import QSvgRenderer
from src.ui.widgets import BannerLabel, WidgetBuilder, FlipButton
from src.ui.widgets import SMAXMAX, SMAXMIN, SMINMAX, SMINMIN, ALEFT, ARIGHT, ATOP, ACENTER
from src.data import DataWrapper
from src.ui.plot import PlotWrapper
import os
import copy

class OscrGui(WidgetBuilder, DataWrapper, PlotWrapper):

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
        self.setup_main_tabber(center)
        self.setup_overview_frame()

    def setup_left_sidebar(self, frame:QFrame):
        left_layout = QVBoxLayout()
        m = self.theme['app']['margin']
        left_layout.setContentsMargins(m, m, m, m)
        left_layout.setSpacing(0)
        left_layout.setAlignment(ATOP)

        head = self.create_label('STO Combatlog:', 'label', frame)
        left_layout.addWidget(head, alignment=ALEFT)

        self.entry = QLineEdit(self.settings['base_path'], frame)
        self.entry.setFixedWidth(self.settings['sidebar_item_width'])
        self.entry.setStyleSheet(self.get_style_class('QLineEdit', 'entry'))
        self.entry.setSizePolicy(SMAXMAX)
        left_layout.addWidget(self.entry)
        
        button_frame = self.create_frame(frame, 'medium_frame')
        button_frame.setSizePolicy(SMINMAX)
        entry_button_config = {
            'default': {'margin-bottom': 15},
            'Browse ...': {'callback': lambda: self.browse_log(self.entry), 'align': ALEFT},
            'Analyze': {'callback': lambda: self.analyze_log_callback(path=self.entry.text()), 'align': ARIGHT}
        }
        entry_buttons = self.create_button_series(button_frame, entry_button_config, 'button')
        button_frame.setLayout(entry_buttons)
        left_layout.addWidget(button_frame)

        gear_button = self.create_icon_button(self.icons['gear'], 'icon_button', frame)
        left_layout.addWidget(gear_button, alignment=ARIGHT)

        background_frame = self.create_frame(frame, 'light_frame', {'border-radius': 2})
        background_frame.setSizePolicy(SMAXMIN)
        background_layout = QVBoxLayout()
        background_layout.setContentsMargins(0, 0, 0, 0)
        background_frame.setLayout(background_layout)
        self.current_combats = QListWidget(background_frame)
        self.current_combats.setStyleSheet(self.get_style_class('QListWidget', 'listbox'))
        self.current_combats.setFont(self.theme_font('listbox'))
        self.current_combats.setSizePolicy(SMAXMIN)
        self.current_combats.setFixedWidth(self.settings['sidebar_item_width'])
        background_layout.addWidget(self.current_combats)
        left_layout.addWidget(background_frame, stretch=1)
        
        gear_button.clicked.connect(lambda: self.analyze_log_callback(self.current_combats.currentRow()))

        frame.setLayout(left_layout)

    def setup_main_tabber(self, frame:QFrame):
        """
        Sets up the tabber switching between Overview, Analysis, League and Settings
        """
        o_frame = self.create_frame(None, 'frame')
        a_frame = self.create_frame(None, 'frame', {'background': 'blue'})
        l_frame = self.create_frame(None, 'frame', {'background': 'pink'})
        s_frame = self.create_frame(None, 'frame', {'background': 'brown'})
        main_tabber = QTabWidget(frame)
        main_tabber.setStyleSheet(self.get_style_class('QTabWidget', 'tabber'))
        main_tabber.tabBar().setStyleSheet(self.get_style_class('QTabBar', 'tabber_tab'))
        main_tabber.setSizePolicy(SMINMIN)
        main_tabber.addTab(o_frame, 'O')
        main_tabber.addTab(a_frame, 'A')
        main_tabber.addTab(l_frame, 'L')
        main_tabber.addTab(s_frame, 'S')
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(main_tabber)
        frame.setLayout(layout)
        self.widgets['main_menu_buttons'][0].clicked.connect(lambda: main_tabber.setCurrentIndex(0))
        self.widgets['main_menu_buttons'][1].clicked.connect(lambda: main_tabber.setCurrentIndex(1))
        self.widgets['main_menu_buttons'][2].clicked.connect(lambda: main_tabber.setCurrentIndex(2))
        self.widgets['main_menu_buttons'][3].clicked.connect(lambda: main_tabber.setCurrentIndex(3))
        self.widgets['main_tab_frames'].append(o_frame)
        self.widgets['main_tab_frames'].append(a_frame)
        self.widgets['main_tab_frames'].append(l_frame)
        self.widgets['main_tab_frames'].append(s_frame)

    def setup_overview_frame(self):
        """
        Sets up the frame housing the combatlog overview
        """
        o_frame = self.widgets['main_tab_frames'][0]
        bar_frame = self.create_frame(None, 'frame')
        dps_graph_frame = self.create_frame(None, 'frame')
        dmg_graph_frame = self.create_frame(None, 'frame')
        self.widgets['overview_tab_frames'].append(bar_frame)
        self.widgets['overview_tab_frames'].append(dps_graph_frame)
        self.widgets['overview_tab_frames'].append(dmg_graph_frame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        switch_frame = self.create_frame(o_frame, 'frame')
        layout.addWidget(switch_frame, alignment=ACENTER)

        o_tabber = QTabWidget(o_frame)
        o_tabber.setStyleSheet(self.get_style_class('QTabWidget', 'tabber'))
        o_tabber.tabBar().setStyleSheet(self.get_style_class('QTabBar', 'tabber_tab'))
        o_tabber.addTab(bar_frame, 'BAR')
        o_tabber.addTab(dps_graph_frame, 'DPS')
        o_tabber.addTab(dmg_graph_frame, 'DMG')
        layout.addWidget(o_tabber)

        switch_style = {
            'default': {'margin-left': '@margin', 'margin-right': '@margin'},
            'DPS Bar': {'callback': lambda: o_tabber.setCurrentIndex(0), 'align':ACENTER},
            'DPS Graph': {'callback': lambda: o_tabber.setCurrentIndex(1), 'align':ACENTER},
            'Damage Graph': {'callback': lambda: o_tabber.setCurrentIndex(2), 'align':ACENTER}
        }
        switches = self.create_button_series(switch_frame, switch_style, 'button')
        switch_frame.setLayout(switches)

        #table

        o_frame.setLayout(layout)


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
            'Overview': {'style':{'margin-left':15}},
            'Analysis': {},
            'League Standings': {},
            'Settings': {},
        }
        bt_lay, buttons = self.create_button_series(menu_frame, menu_button_style, 
                style='menu_button', seperator='•', ret=True)
        menu_frame.setLayout(bt_lay)
        self.widgets['main_menu_buttons'] = buttons

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
        pos_x = int(rel_x * width)
        pos_y = int(rel_y * height)
        width = int(rel_size_x * width)
        height = int(rel_size_y * height)
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

    def analyze_log_callback(self, combat_id=None, path=None):
        """wrapper function for retrieving and showing data"""
        # initial run / click on the Analyze button
        if combat_id is None:
            if not path or not os.path.isfile(path):
                self.show_warning('Invalid Logfile', 'The Logfile you are trying to open does not exist.')
                return
            combats = self.get_data(combat=None, path=path)
            self.current_combats.clear()
            self.current_combats.addItems(combats)
            self.current_combats.setCurrentRow(0)
            self.current_combat_id = 0
            
            self.create_overview()
        # subsequent run / click on older combat
        elif isinstance(combat_id, int) and combat_id != self.current_combat_id: 
            self.get_data(combat_id)
            self.create_overview()
            self.current_combat_id = combat_id