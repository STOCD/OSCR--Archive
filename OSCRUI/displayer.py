

from PyQt6.QtWidgets import QVBoxLayout, QWidget, QTableView

from .datamodels import TableModel, SortingProxy
from .widgetbuilder import SMPIXEL, RFIXED, SMINMIN
from .style import get_style_class

def create_overview(self):
    """
    creates the main Parse Overview including graphs and table
    """
    # clear graph frames
    for frame in self.widgets['overview_tab_frames']:
        if frame.layout():
            QWidget().setLayout(frame.layout())

    # close graphs
    """for figure in self.widgets['overview_graphs']:
        plt.close(figure)
    self.widgets['overview_graphs'] = []"""

    # DPS Bar Graph
    #l = self.create_overview_bars()
    # DPS Graph
    #self.create_overview_dps()
    # DMG Bars
    """self.widgets['overview_menu_buttons'][2].setDisabled(True)
    dmg_thread = CustomThread(self.window, self.create_overview_dmg)
    dmg_thread.result.connect(self.slot_overview_dmg)
    dmg_thread.start()"""

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    self.widgets['overview_tab_frames'][0].setLayout(layout)
    
    # Overview Table
    tbl = create_overview_table(self)
    layout.addWidget(tbl, stretch=4)

def create_overview_table(self) -> QTableView:
    """
    Creates the overview table and returns it.

    :return: Overview Table
    """
    model = TableModel(self.parser1.active_combat.table,
            header_font=self.theme_font('table_header'), cell_font=self.theme_font('table'))
    sort = SortingProxy()
    sort.setSourceModel(model)
    table = QTableView(self.widgets['overview_tab_frames'][0])
    table.setAlternatingRowColors(self.theme['s.c']['table_alternate'])
    table.setShowGrid(self.theme['s.c']['table_gridline'])
    table.setSortingEnabled(True)
    table.setModel(sort)
    table.setStyleSheet(get_style_class(self, 'QTableView', 'table'))
    table.setHorizontalScrollMode(SMPIXEL)
    table.setVerticalScrollMode(SMPIXEL)
    table.horizontalHeader().setStyleSheet(get_style_class(self, 'QHeaderView', 'table_header'))
    table.verticalHeader().setStyleSheet(get_style_class(self, 'QHeaderView', 'table_index'))
    table.resizeColumnsToContents()
    for col in range(len(model._header)):
        table.horizontalHeader().resizeSection(col, table.horizontalHeader().sectionSize(col) + 5)
    table.resizeRowsToContents()
    table.horizontalHeader().setSectionResizeMode(RFIXED)
    table.verticalHeader().setSectionResizeMode(RFIXED)
    table.setSizePolicy(SMINMIN)
    return table