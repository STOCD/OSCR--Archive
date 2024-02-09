import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QTableView
import numpy as np

from .data import TableModel, SortingProxy
from .widgets import SMINMIN, RFIXED, SMPIXEL
from .lib import clean_player_id, CustomThread

class PlotWrapper():

    from .styles import theme_font, get_style_class

    def __init__(self) -> None:
        """
        This class is not inteded to be instantiated.
        """
        return

    def create_overview(self):
        """
        creates the main Parse Overview including graphs and table
        """
        # clear graph frames
        for frame in self.widgets['overview_tab_frames']:
            if frame.layout():
                QWidget().setLayout(frame.layout())

        # close graphs
        for figure in self.widgets['overview_graphs']:
            plt.close(figure)
        self.widgets['overview_graphs'] = []

        # DPS Bar Graph
        l = self.create_overview_bars()
        # DPS Graph
        self.create_overview_dps()
        # DMG Bars
        self.widgets['overview_menu_buttons'][2].setDisabled(True)
        dmg_thread = CustomThread(self.window, self.create_overview_dmg)
        dmg_thread.result.connect(self.slot_overview_dmg)
        dmg_thread.start()

        # Overview Table
        tbl = self.create_overview_table()
        l.addWidget(tbl, stretch=4)

    def create_overview_dmg(self) -> Figure:
        """
        Adds data to matplotlib bar chart.

        :return: matplotlib figure with inserted data
        """
        with plt.style.context(self.config['plot_stylesheet_path']):
            f, a = self.create_grouped_bar_plot(self.overview_data[4])
            a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.025), ncol=3, frameon=False)
            a.set_xlabel('[s]', loc='right')
        return f

    def slot_overview_dmg(self, result):
        """
        Inserts the figure into the UI

        Parameters:
        - :param result: tuple containing the matplotlib figure to be inserted
        """
        figure = result[0]
        self.widgets['overview_graphs'].append(figure)
        dmg_chart = FigureCanvasQTAgg(figure)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(dmg_chart)
        self.widgets['overview_tab_frames'][2].setLayout(layout)
        self.widgets['overview_menu_buttons'][2].setDisabled(False)

    def create_overview_dps(self):
        """
        Adds data to matplotlib graph chart and inserts the figure into the UI.
        """
        with plt.style.context(self.config['plot_stylesheet_path']):
            f, a = plt.subplots()
            for player, array in self.overview_data[3].items():
                a.plot(np.divide(array[0], 1000), array[1], 
                        label=clean_player_id(player))
            a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.025), ncol=3, frameon=False)
            a.set_xlabel('[s]', loc='right')
        
        self.widgets['overview_graphs'].append(f)
        dps_chart = FigureCanvasQTAgg(f)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(dps_chart)
        self.widgets['overview_tab_frames'][1].setLayout(layout)

    def create_overview_bars(self) -> QVBoxLayout:
        """
        Adds data to matplotlib horizontal bar chart and inserts the figure into the UI.

        :return: layout with inserted figure
        """
        dps = self.get_overview_dps()
        players = self.overview_data[2]
        y = np.arange(len(players))
        lbs = self.format_bar_labels(dps)
        with plt.style.context(self.config['plot_stylesheet_path']):
            f, a = plt.subplots()
            bars = a.barh(y, dps, align='center', color=self.theme['defaults']['mfg'])
            a.set_yticks(y, labels=players)
            self.create_bar_labels(a, bars, y, lbs, dps)
        
        self.widgets['overview_graphs'].append(f)
        chart = FigureCanvasQTAgg(f)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(chart, stretch=11)
        self.widgets['overview_tab_frames'][0].setLayout(layout)

        return layout
    
    def create_bar_labels(self, axis: Axes, bars, y, names, x):
        """
        Adds bar labels to horizontal bar chart. Labels are placed inside the bar left-aligned by default.
        Bars smaller than 10% of the widest bar are labeled outside of the bar aligned to its right edge.

        Parameters:
        - :param axis: Axes -> the plot containing the bars
        - :param bars: BarContainer -> contains the bars themselves
        - :param y: iterable of positions on the vertical axis where labels are added
        - :param names: iterable of the label texts
        - :param x: iterable of the width of the bars
        """
        x_thre = max(x)//10
        x_pos = max(x)//100
        labels = []
        for pos, name, mag in zip(y, names, x):
            if mag > x_thre:
                axis.text(x_pos, pos, name, verticalalignment='center_baseline', 
                        fontsize=17, fontweight='bold')
                labels.append('')
            else:
                labels.append(name)
        axis.bar_label(bars, labels=labels, color=self.theme['defaults']['fg'], fontsize=17,
                padding=self.theme['defaults']['margin'], label_type='edge', fontweight='bold')

    def format_bar_labels(self, values):
        """formats bar labels; '1000' becomes '1 k', '1000000' becomes '1 M'"""
        labels = []
        for v in values:
            if v > 1000000:
                labels.append(f'{v/1000000:.2f} M')
            elif v > 1000:
                labels.append(f'{v/1000:.2f} k')
            else:
                labels.append(f'{v:.2f}')
        return labels

    def get_overview_dps(self):
        """
        Retrieves DPS values from self.overview_data

        :return: 
        """
        return np.array([el[1] for el in self.overview_data[0]])

    def create_grouped_bar_plot(self, data: dict) -> tuple[Figure, Axes]:
        """
        Creates a bar plot with grouped bars and returns figure and axis.

        Parameters:
        - :param data: dictionary contining multiple sets of data

        :return: Figure and Axes with inserted data
        """
        f, a = plt.subplots()
        group_width = 0.18 # distance between data points
        num = len(data)
        wd = group_width / num
        positions = np.arange(0, group_width, wd)
        offsets = positions - np.median(positions)
        for off, (player, ar) in zip(offsets, data.items()):
            x = np.divide(ar[0], 1000) + off
            a.bar(x, ar[1], label=clean_player_id(player), width=wd)
        return f, a

    def create_overview_table(self) -> QTableView:
        """
        Creates the overview table and returns it.

        :return: Overview Table
        """
        model = TableModel(*self.overview_data[0:3],
                header_font=self.theme_font('table_header'), cell_font=self.theme_font('table'))
        sort = SortingProxy()
        sort.setSourceModel(model)
        table = QTableView(self.widgets['overview_tab_frames'][0])
        table.setAlternatingRowColors(self.theme['s.c']['table_alternate'])
        table.setShowGrid(self.theme['s.c']['table_gridline'])
        table.setSortingEnabled(True)
        table.setModel(sort)
        table.setStyleSheet(self.get_style_class('QTableView', 'table'))
        table.setHorizontalScrollMode(SMPIXEL)
        table.setVerticalScrollMode(SMPIXEL)
        table.horizontalHeader().setStyleSheet(self.get_style_class('QHeaderView', 'table_header'))
        table.verticalHeader().setStyleSheet(self.get_style_class('QHeaderView', 'table_index'))
        table.resizeColumnsToContents()
        for col in range(len(model._header)):
            table.horizontalHeader().resizeSection(col, table.horizontalHeader().sectionSize(col) + 5)
        table.resizeRowsToContents()
        table.horizontalHeader().setSectionResizeMode(RFIXED)
        table.verticalHeader().setSectionResizeMode(RFIXED)
        table.setSizePolicy(SMINMIN)
        return table
