from tkinter import Frame, Label, Button, Canvas, Tk, Entry, Text
from tkinter import TOP, BOTTOM, X, Y, LEFT, RIGHT, CENTER, BOTH, VERTICAL, HORIZONTAL
#from tkinter import Scrollbar
from tkinter.ttk import Scrollbar, Style
from platform import system



class Easytable(Frame):

    # external functions section

    def configure_borders(self, target:str, top_border:int=0, bottom_border:int=0, left_border:int=0, right_border:int=0):
        """target: one of the following: 
            'heading' (to target the heading),
            'content' (to target the whole content),
            'row?' (to target a specific row, example'row4', this parameter has to be the last element of the string), 
            'column?' (see row)

            'heading' and 'content' might be used together
            'row?' and 'column?' only affect content, but may not be used together
            """
        if 'heading' in target:
            self._configure_row_borders(-1, (left_border,right_border), (top_border,bottom_border), heading=True)
        if 'content' in target and not 'row' in target and not 'column' in target:
            self._configure_content_borders((left_border,right_border), (top_border,bottom_border))
        elif 'content' in target and 'row' in target:
            row = int(target[target.find('row')+3:])
            try:
                self._configure_row_borders(row, (left_border,right_border), (top_border,bottom_border))
            except IndexError: pass
        elif 'content' in target and 'column' in target:
            column = int(target[target.find('column')+6:])
            try:
                self._configure_column_borders(column, (left_border,right_border), (top_border,bottom_border))
            except IndexError: pass
        self._align_column_width()

    def configure_style(self, target:str, cell_style:dict):
        """target: meaningful concenation of a selection of the following strings:
            'heading' (target the heading),
            'content' (target the whole content),
            'row?' (target a specific row, example'row4', this parameter has to be the last element of the string),
            'column?' (see row), -> row and column may not be used together! (use cell instead),
            'cell[?,?]' (target specific cell of the content, replace question marks with row and column; -> use 'heading column?' for a cell in the heading)
            'pattern[?]': (target rows and columns to create a pattern on the content, not usable together with row, column or cell)
            
        """
        if len(target) < 1 and len(cell_style) < 1:
            return

        if 'cell' in target:
            row_id = int(target[target.find('cell[')+5:])
            col_id = int(target[target.find(',')+1:target.find(']')])
            self._configure_cell(row=row_id, col=col_id, cell_style=cell_style)
        elif 'pattern' in target:
            pattern = target[target.find('pattern[')+8:target.find(']')]
            if 'oddrows' in pattern:
                for i in self.get_keys(self._cells['rows']):
                    if (i % 2) == 1:
                        self._configure_row_cells(i, cell_style)
            elif 'evenrows' in pattern:
                for i in self.get_keys(self._cells['rows']):
                    if (i % 2) == 0:
                        self._configure_row_cells(i, cell_style)
        else:
            if 'heading' in target:
                if 'column' in target:
                    self._configure_cell(row=0, col=int(target[target.find('column')+6:]), cell_style=cell_style, heading=True)
                else:
                    self._configure_row_cells(row_id=0, cell_style=cell_style, heading=True)
            elif 'content' in target:
                if 'row' in target:
                    self._configure_row_cells(row_id=int(target[target.find('row')+3:]), cell_style=cell_style)
                elif 'column' in target:
                    self._configure_column_cells(column_id=int(target[target.find('column')+6:]), cell_style=cell_style)
                else:
                    self._configure_content_cells(cell_style=cell_style)

    # internal section

    _cells = {
        'headings':{
            '_frame': None,
            '_canvas': None
        },
        'rows':{
            '_frame': None,
            '_canvas': None
        }
    }

    _paddings = {
        'headings':{},
        'rows':{}
    }

    _scroll_frames = {
        'headings': None,
        'content': None,
    }

    def __init__(self, master, columns: list = [], heading_style: dict = {}, cell_style: dict = {}, scrollbar_style:dict = {}, border_color = 'black', **kw):
        Frame.__init__(self, master=master, **kw)
        self._init_style(scrollbar_style)
        self._init_grid(len(columns), border_color)
        self._init_columns(columns, heading_style)

    def _init_grid(self, col, border_color):

        v_scroll = Scrollbar(self, orient=VERTICAL, style='C.Vertical.TScrollbar')
        v_scroll.pack(side=RIGHT, fill=Y)
        h_scroll = Scrollbar(self, orient=HORIZONTAL, style='C.Horizontal.TScrollbar')
        

        header = ScrollableFrame(self, orient=HORIZONTAL, scroll_slave=True, ex_h_sb=h_scroll, color=border_color)
        header.pack(side=TOP, fill=X)
        header.pack_propagate(False)
        for i in range(col+1):
            header.sf.columnconfigure(i, weight=0)
        header.sf.rowconfigure(0, weight=0)
        header.sf.rowconfigure(1, weight=0)
        self._cells['headings']['_frame'] = header.sf
        self._cells['headings']['_canvas'] = header.canvas
        self._scroll_frames['headings'] = header

        content = ScrollableFrame(self, orient=BOTH, scroll_slave=True, ex_h_sb=h_scroll, ex_v_sb=v_scroll, color=border_color)
        content.pack(side=TOP, fill=X)
        self._cells['rows']['_frame'] = content.sf
        self._cells['rows']['_canvas'] = content.canvas
        self._scroll_frames['content'] = content

        self.scroll_commands = [header.canvas.xview, content.canvas.xview]
        v_scroll.configure(command=content.canvas.yview)
        h_scroll.configure(command=self._multi_scroll)
        h_scroll.pack(side=TOP, fill=X)
        content.sf.bind('<MouseWheel>', self._bind_scroll)

    def _init_style(self, scrollbar_style):
        trough = {'troughcolor':'#888888','troughrelief':'flat','borderwidth':0}
        arrow = {'background':'#555555', 'relief':'flat', 'borderwidth':0, 'arrowcolor':'#000000'}
        thumb = {'relief':'flat', 'background':'#555555', 'borderwidth':0}
        if 'trough' in scrollbar_style:
            trough = scrollbar_style['trough']
        if 'arrow' in scrollbar_style:
            arrow = scrollbar_style['arrow']
        if 'thumb' in scrollbar_style:
            thumb = scrollbar_style['thumb']
        style = Style()
        style.theme_use('default')
        style.configure('C.Horizontal.TScrollbar', **trough)
        style.configure('C.Horizontal.TScrollbar', **arrow)
        style.configure('C.Horizontal.TScrollbar', **thumb)
        style.configure('C.Vertical.TScrollbar', **trough)
        style.configure('C.Vertical.TScrollbar', **arrow)
        style.configure('C.Vertical.TScrollbar', **thumb)

    def _multi_scroll(self, *args):
        for func in self.scroll_commands:
            func(*args)

    def _init_columns(self, cols, heading_style: dict = {}):
        header: Frame = self._cells['headings']['_frame']
        for i, e in enumerate(cols):
            header.grid_columnconfigure(i, weight=0)
            head = Label(header, text=e, **heading_style)
            head.grid(row=0, column=i, sticky='nsew', ipadx=3, ipady=3)
            self._cells['headings'][i] = head
            self._paddings['headings'][i] = (0, 0, 0, 0)
        self._set_height(1, True)

    def _add_row(self, row_data: list, cell_style: dict = {}):
        row_to_insert = len(self.get_keys(self._cells['rows']))
        frame: Frame = self._cells['rows']['_frame']
        row = list()
        for i in range(len(self._cells['headings'])-2):
            try:
                l = Label(frame, text=row_data[i], relief='flat', **cell_style)
                l.grid(row=row_to_insert, column=i, sticky='nsew', ipadx=3, ipady=3)
                l.bind('<MouseWheel>', self._bind_scroll)
                row.append(l)
            except IndexError:
                break 
        self._cells['rows'][row_to_insert] = row
        self._paddings['rows'][row_to_insert] = [(0, 0, 0, 0) for j in range(len(row))]

        self._align_column_width()

    def _configure_row_cells(self, row_id: int, cell_style: dict = {}, heading = False):
        if row_id < 0 or len(cell_style) < 1:
            return
        if not heading:
            row = self._cells['rows'][row_id]
            for cell in row:
                cell.configure(**cell_style)
        else:
            for cell_id in self.get_keys(self._cells['headings']):
                self._cells['headings'][cell_id].configure(**cell_style)

    def _configure_column_cells(self, column_id: int, cell_style: dict = {}):
        if column_id < 0 or len(cell_style) < 1:
            return
        for row_id in self.get_keys(self._cells['rows']):
            self._cells['rows'][row_id][column_id].configure(**cell_style)

    def _configure_cell(self, row = 0, col = 0, cell_style: dict = {}, heading=False):
        if row < 0 or col < 0 or len(cell_style) < 1:
            return
        if not heading:
            self._cells['rows'][row][col].configure(**cell_style)
        else:
            self._cells['headings'][col].configure(**cell_style)

    def _configure_content_cells(self, cell_style: dict = {}):
        for row_id in self.get_keys(self._cells['rows']):
            self._configure_row_cells(row_id, cell_style)
        self._align_column_width()

    def _merge_padding(self, inherit:tuple, new:tuple):
        """paddings must be formatted as: (left, right, top, bottom)"""
        result = tuple()
        for i, pad in enumerate(new):
            if pad is None:
                result = (*result, inherit[i])
            else:
                result = (*result, pad)
        return result

    def _configure_content_cell_padding(self, row, col, x_padding:tuple = (None,None), y_padding:tuple = (None,None)):
        padding = self._merge_padding(self._paddings['rows'][row][col], (x_padding[0], x_padding[1], y_padding[0], y_padding[1]))
        self._paddings['rows'][row][col] = padding
        cell : Label = self._cells['rows'][row][col]
        cell.grid_configure( padx=(padding[0], padding[1]), pady=(padding[2], padding[3]) )

    def _configure_heading_cell_padding(self, col, x_padding:tuple = (None,None), y_padding:tuple = (None,None)):
        padding = self._merge_padding(self._paddings['headings'][col], (x_padding[0], x_padding[1], y_padding[0], y_padding[1]))
        self._paddings['headings'][col] = padding
        cell : Label = self._cells['headings'][col]
        cell.grid_configure(padx=x_padding, pady=y_padding)

    def _configure_row_borders(self, row_num, x_borders:tuple = (None,None), y_borders:tuple = (None,None), heading=False):
        if not heading:
            for col in range(len(self._cells['rows'][row_num])):
                self._configure_content_cell_padding(row_num, col, x_borders, y_borders)
        else:
            for col in range(len(self._cells['headings'])-2):
                self._configure_heading_cell_padding(col, x_borders, y_borders)

    def _configure_column_borders(self, col_num, x_borders:tuple = (None,None), y_borders:tuple = (None,None)):
        for row_num in range(len(self._cells['headings']-2)):
            self._configure_content_cell_padding(row_num, col_num, x_borders, y_borders)

    def _configure_content_borders(self, x_borders:tuple = (None,None), y_borders:tuple = (None,None)):
        for row_num in self.get_keys(self._cells['rows']):
            self._configure_row_borders(row_num, x_borders, y_borders)


    def _align_column_width(self):
        header_columns = self.get_keys(self._cells['headings'])
        rows = self.get_keys(self._cells['rows'])
        if len(rows) < 1:
            return
        max_width = [0 for i in range(len(header_columns))]
        for row in rows:
            for i, cell in enumerate(self._cells['rows'][row]):
                cell.update()
                if (cell.winfo_width() + sum(self._paddings['rows'][row][i][:2])) > max_width[i]:
                    max_width[i] = cell.winfo_width() + sum(self._paddings['rows'][row][i][:2])
        for col in header_columns:
            self._cells['headings'][col].update()
            if (self._cells['headings'][col].winfo_width() + sum(self._paddings['headings'][col][:2])) > max_width[col]:
                self._cells['rows']['_frame'].grid_columnconfigure(col, minsize=(self._cells['headings'][col].winfo_width() + sum(self._paddings['headings'][col][:2])))
            else:
                self._cells['headings']['_frame'].grid_columnconfigure(col, minsize=max_width[col])

    def _bind_scroll(self, event):
        if system() == 'Darwin':
            self._cells['rows']['_canvas'].yview_scroll(int(event.delta), 'units')
        elif system() == 'Windows':
            self._cells['rows']['_canvas'].yview_scroll(int(-1*(event.delta/120)), 'units')

    def _set_height(self, lines, header=False):
        if header:
            self._cells['headings'][0].update()
            height = self._cells['headings'][0].winfo_height() + sum(self._paddings['headings'][0][2:])
            self._scroll_frames['headings'].configure(height=height)
        else:
            self._cells['rows'][0][0].update()
            height = self._cells['rows'][0][0].winfo_height() + sum(self._paddings['rows'][0][0][2:])
            self._scroll_frames['content'].pack_propagate(False)
            self._scroll_frames['content'].configure(height=height*lines)

    def get_keys(self, d:dict):
        keys = []
        for key in d.keys():
            if isinstance(key, int):
                keys.append(key)
        return keys


class ScrollableFrame(Frame):
    def __init__(self, container, orient=VERTICAL, scroll_slave=False, ex_h_sb:Scrollbar= None,ex_v_sb:Scrollbar= None, color=None, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self, relief='flat')
        if not scroll_slave:
            if orient == VERTICAL: scroll_command = self.canvas.yview
            elif orient == HORIZONTAL: scroll_command = self.canvas.xview
            self.scrollbar = Scrollbar(self, orient=orient, command=scroll_command)
        self.sf = Frame(self.canvas, background=color)

        self.sf.bind(
            "<Configure>",
            lambda e: self.__adjust_scrollregion()
        )


        self.canvas.create_window((-1, -1), window=self.sf, anchor="nw")

        if not scroll_slave:
            if orient == VERTICAL:
                self.canvas.configure(yscrollcommand=self.scrollbar.set)
                direc = Y
                pack_side = LEFT
            elif orient == HORIZONTAL:
                self.canvas.configure(xscrollcommand=self.scrollbar.set)
                direc = X
                pack_side = TOP
            self.canvas.pack(side=pack_side, fill="both", expand=True, anchor='nw')
        else:
            if orient == VERTICAL:
                self.canvas.configure(yscrollcommand=ex_v_sb.set)
            elif orient == HORIZONTAL:
                self.canvas.configure(xscrollcommand=ex_h_sb.set)
            elif orient == BOTH:
                self.canvas.configure(yscrollcommand=ex_v_sb.set)
                self.canvas.configure(xscrollcommand=ex_h_sb.set)
            self.canvas.pack(side=LEFT, fill="both", expand=True, anchor='nw')

        if not scroll_slave:
            self.scrollbar.pack(side=pack_side, fill=direc)

    def __adjust_scrollregion(self):
        scr = self.canvas.bbox('all')
        scr = (1, 1, scr[2]-2, scr[3]-2)
        self.canvas.configure(scrollregion=scr)