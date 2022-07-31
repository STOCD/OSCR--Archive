import tkinter
import statistics
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Progressbar
from tkinter import Tk, messagebox, Toplevel
from tkinter import PhotoImage, font, StringVar
from tkinter import Frame, Label, Entry, OptionMenu
from tkinter import BOTH, BOTTOM, DISABLED, END, FLAT, HORIZONTAL, CENTER
from tkinter import LEFT, NORMAL, RIGHT, TOP, VERTICAL, WORD, X, Y
import sys
import os
import json
from PIL import Image, ImageTk, ImageGrab
from operator import itemgetter
from decimal import Decimal
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tksheet import Sheet as TkSheet
from local.Easytable import Easytable

import OSCR

class OSCRUI():


    # save theme here
    theme = {
        'app':{
            'font': {
                'family': 'Helvetica',
                'size': 10,
                'weight': '',
                'tuple': ('Helvetica', 10, 'bold')
            },
            'bg': '#3a3a3a',
            'text': '#b3b3b3',
            'oscr': '#c82934', #b81924,
            'accent': '#aa3c3c',
            'light_bg': '#555555'
        },
        'bar':{
            'font':{
                'weight': 'bold',
                'size': 13
            },
            'fg': '#888888',
            'bg': '#424242',
            'light_text':'#e0e0e0',
            'dark_text': '#222222'
        },
        'scroll':{
            'trough':{'troughcolor':'#424242','troughrelief':'flat','borderwidth':0},
            'arrow':{'background':'#888888', 'relief':'flat', 'borderwidth':0, 'arrowcolor':'#3a3a3a'},
            'thumb':{'relief':'flat', 'background':'#888888', 'borderwidth':0}
        },
        'table':{
            'heading':{'font':('Helvetica',15,'normal'), 'fg':'#b3b3b3', 'bg':'#3a3a3a'},
            'content':{'bg':'#424242', 'fg':'#e0e0e0', 'font':('Helvetica',15,'bold'), 'anchor':'e', 'padx':5},
            'bordercolor': '#222222',
            'borderwidth':{'top_border':0, 'bottom_border':0, 'left_border':0, 'right_border':1},
            'altcolor': '#3a3a3a'
        },
        'button':{
            'fg':'#e0e0e0',
            'bg':'#424242',
            'bd':'#222222',
            'hover':'#c82934',
            'font':('Helvetica',13,'normal')
        },
        'label':{
            'bg':'#3a3a3a',
            'fg':'#e0e0e0',
            'font':('Helvetica', 14, 'normal')
        },
        'entry':{
            'bg':'#555555',
            'fg':'#e0e0e0',
            'font':('Helvetica', 13, 'normal'),
            'relief':'flat',
            'highlightbackground':'#222222',
            'highlightthickness':1,
            'highlightcolor':'#c82934',
            'exportselection':0,
            'selectbackground':'#aa3c3c',
            'selectforeground':'#e0e0e0'
        }
    }

    # table theme -- do not change keys!
    theme_table = {

        'popup_menu_fg': "white",
        'popup_menu_bg': "gray15",
        'popup_menu_highlight_bg': "gray35",
        'popup_menu_highlight_fg': "white",

        'index_hidden_rows_expander_bg': "gray30",
        'header_hidden_columns_expander_bg': "gray30",

        'header_bg': "#3a3a3a",
        'header_border_fg': "#222222",
        'header_grid_fg': "#222222",
        'header_fg': "#b3b3b3", 
        'header_selected_cells_bg': "#3a3a3a",
        'header_selected_cells_fg': "#b3b3b3",

        'index_bg': "#3a3a3a",
        'index_border_fg': "#222222",
        'index_grid_fg': "#222222",
        'index_fg': "#b3b3b3",
        'index_selected_cells_bg': "#3a3a3a",
        'index_selected_cells_fg': "#b3b3b3",

        'top_left_bg': "#3a3a3a",
        'top_left_fg': "#b3b3b3",
        'top_left_fg_highlight': "#c2c9cf",

        'table_bg': "#3a3a3a",
        'table_grid_fg': "#222222",
        'table_fg': "#e0e0e0",
        'table_selected_cells_border_fg': "#c82934",
        'table_selected_cells_bg': "#3a3a3a",
        'table_selected_cells_fg': "#e0e0e0",

        'resizing_line_fg': "white",
        'drag_and_drop_bg': "white",
        'outline_color': "#ffff00",

        'header_selected_columns_bg': "#3a3a3a",
        'header_selected_columns_fg': "#b3b3b3",

        'index_selected_rows_bg': "#3a3a3a",
        'index_selected_rows_fg': "#b3b3b3",

        'table_selected_rows_border_fg': "#c82934",
        'table_selected_rows_bg': "#3a3a3a",
        'table_selected_rows_fg': "#e0e0e0",
        'table_selected_columns_border_fg': "#c82934",
        'table_selected_columns_bg': "#3a3a3a",
        'table_selected_columns_fg': "#e0e0e0"
    }

    # default settings
    settings = {
        'log_path':''
    }

    def get_data(self):
        self.players = {}
        self.overviewData = [[],[],[]]
        brain = OSCR.parser()
        data1, *trash = brain.readCombatwithUITables(self.log_path.get())
        data4 = brain.createFrontPageTable()

        for line in data4[1:]:
            self.overviewData[0].append(line[1:])
            self.overviewData[2].append(line[0])

        self.overviewData[1] = data4[0][1:]
        for key in data1.keys():
            if key[0] == 'P':
                player_abilities = []
                for ability in data1[key][1]:
                    player_abilities.append([ability[0][0], *ability[0][2:]])
                player_abilities = sorted(player_abilities, key=itemgetter(2), reverse=True)
                self.players[key[key.find(' ')+1:-1]] = player_abilities
        

    def open_combat_analysis(self):
        c_analysis = Toplevel(self.window, bg=self.theme['app']['oscr'])
        c_analysis.transient(self.window)
        c_analysis.geometry('1000x600')
        c_analysis.title('OSCR - Combat Analysis')
        
        analysis_frame = Frame(c_analysis, bg=self.theme['app']['bg'], highlightthickness=0)
        analysis_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)
        analysis_frame.grid_columnconfigure(0, weight=1)
        analysis_frame.grid_columnconfigure(1, weight=0)
        analysis_frame.grid_rowconfigure(0, weight=0)
        analysis_frame.grid_rowconfigure(1, weight=1)
        analysis_frame.grid_rowconfigure(2, weight=0)

        table_frame = Frame(analysis_frame, bg=self.theme['app']['bg'], highlightthickness=0)
        table_frame.grid(row=1, column=0, sticky='nsew')
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_rowconfigure(1, weight=0)
        table_frame.pack_propagate(False)

        player_list = list(self.players.keys())
        table_dict = {}
        cols = ['Name', 'Damage', 'DPS', 'Max One Hit', 'Crits', 'Flanks', 'Attacks', 'Misses', 'CrtH', 'Accuracy', 
                'Flank Rate', 'Kills', 'Hull Damage', 'Shield Damage', 'Resistance', 'Hull Attacks', 'Final Resist']
        for player in player_list:
            player_table = self.create_table(table_frame, data=self.players[player], headers=cols)
            table_dict[player] = player_table
            """#print(player)
            #go = time.perf_counter()
            player_table = Easytable(table_frame, columns=cols, 
                    border_color=self.theme['table']['bordercolor'],
                    heading_style=self.theme['table']['heading'], scrollbar_style=self.theme['scroll'],
                    bg=self.theme['app']['bg'])
            #print(f'after constructor: {time.perf_counter()-go}')
            player_table.add_content(self.players[player], self.format_data)
            #print(f'after add_content: {time.perf_counter()-go}')
            player_table.style_configure('content', self.theme['table']['content'])
            #print(f'after style: {time.perf_counter()-go}')
            player_table.border_configure('heading content', **self.theme['table']['borderwidth'])
            #print(f'after border1: {time.perf_counter()-go}')
            player_table.border_configure('heading', bottom_border=2)
            #print(f'after border2: {time.perf_counter()-go}')
            player_table.style_configure('pattern[oddrows]', {'bg':self.theme['table']['altcolor']})
            #print(f'after style2: {time.perf_counter()-go}')
            table_dict[player] = player_table"""

        current_player = StringVar(c_analysis, player_list[0])
        current_player.trace_add('write', lambda e1, e2, e3: self.c_a_changed_player(table_dict, current_player.get()))
        player_selector = OptionMenu(analysis_frame, current_player, *player_list)
        player_selector.configure(background=self.theme['app']['bg'], font=self.theme['button']['font'])
        player_selector.grid(row=0, column=0, sticky='nw')
        table_dict[player_list[0]].pack(fill=BOTH, expand=True)


    def c_a_changed_player(self, tables, change_to):
        if tables[change_to].winfo_ismapped(): 
            return
        for child in tables:
            if tables[child].winfo_ismapped():
                tables[child].pack_forget()
                tables[change_to].pack(fill=BOTH, expand=True)

    def analyze_log(self):
        if not os.path.exists(self.log_path.get()):
            messagebox.showerror(title='Invalid Path', message='The filepath you entered is invalid!')
            return
        self.make_splash()
        self.get_data()
        self.create_overview()
        self.terminate_splash()

    def create_overview(self):

        for current_frame in [self.dps_bar_frame, self.overview_table_frame]:
            self.clear_frame(current_frame) 

        dps = [el[1] for el in self.overviewData[0]]
        x = self.overviewData[2]
        lbs = self.format_bar_labels(dps)
        with plt.style.context(self.resource_path('local/oscr_default.mplstyle')):
            f, a = plt.subplots()
            bars = [a.barh(x[j], dps[j], color=self.theme['bar']['fg']) for j in range(len(dps))]
            for i, bar in enumerate(bars):
                self.create_bar_label(bar, a, dps, dps[i], lbs[i], i)
            f.set_figwidth(int(self.windowWidth*0.075))
        #plt.tight_layout()
        chart = FigureCanvasTkAgg(f, self.dps_bar_frame).get_tk_widget()
        chart.pack(fill=BOTH, ipadx=100, ipady=0)

        self.format_table(self.overviewData[0])

        overview_table = self.create_table(self.overview_table_frame, *self.overviewData)
        overview_table.grid(row=0, column=0, sticky='nsew')
        overview_table.grid_propagate(False)
        table_height = overview_table.get_row_heights()[0] * 6.75
        overview_table.configure(height=table_height)

        """tree_frame = Frame(self.contentFrame, highlightbackground=self.theme['table']['bordercolor'], 
                highlightthickness=1)
        tree_frame.grid(row=2, column=0, sticky='new', padx=(60,30), pady=30, columnspan=2)
        table = Easytable(tree_frame, columns=self.overviewTableHeaders, border_color=self.theme['table']['bordercolor'],
                heading_style=self.theme['table']['heading'], scrollbar_style=self.theme['scroll'])
        table.pack(fill=X)
        table.add_content(self.overviewData, self.format_data)
        table.style_configure('content', self.theme['table']['content'])
        table.border_configure('heading content', **self.theme['table']['borderwidth'])
        table.border_configure('heading', bottom_border=2)
        table.style_configure('pattern[oddrows]', {'bg':self.theme['table']['altcolor']})
        table.table_configure(height=5)"""

    def create_table(self, parent, data, headers=None, index=None):
        table = TkSheet(parent=parent, data=data, empty_horizontal=0, empty_vertical=0, header_font=self.theme['table']['heading']['font'], font=self.theme['table']['content']['font'])
        table.enable_bindings('single_select', 'drag_select', 'column_select', 'row_select')
        table.set_all_row_heights(height=30, redraw=False)
        table.align('e', redraw=False)
        if headers is not None:
            table.headers(newheaders=headers)
        if index is not None:
            table.row_index(newindex=index)
        table.set_all_column_widths(redraw=False)
        table.set_width_of_index_to_text()
        table.MT.display_selected_fg_over_highlights = False
        table.set_options(**self.theme_table, redraw = True)
        table.config(bg = self.theme_table['table_bg'])
        return table

    def format_table(self, t):
        for i in t:
            for j in range(len(i)):
                i[j] = self.format_data(i[j])

    def format_data(self, el):
        if isinstance(el, (int, float)):
            a = Decimal(el).quantize(Decimal('1.00'))
            return f'{a:,}'
        else:
            return str(el)        

    def create_bar_label(self, bar, axis: Axes , data, current, label, n):
        if current > max(data)/10:
            color = self.theme['bar']['dark_text']
            axis.text(max(data)/100,n-.08,label,color=color, fontweight=self.theme['bar']['font']['weight'], 
                    fontsize=self.theme['bar']['font']['size'])

        else:
            color = self.theme['bar']['light_text']
            axis.bar_label(bar, labels=[label], label_type='edge', fontweight=self.theme['bar']['font']['weight'], 
                    fontsize=self.theme['bar']['font']['size'], color=color, padding=5)
        
    def format_bar_labels(self, values):
        labels = []
        for v in values:
            if v > 1000000:
                v = round(v/1000000, 2)
                labels.append(f'{v} M')
            elif v > 1000:
                v = round(v/1000, 2)
                labels.append(f'{v} K')
            else:
                v = round(v, 2)
                labels.append(str(v))
        return labels

    def create_default_button(self, master, text, command, **kwargs):
        button = PlainButton(master, text=text, highlightthickness=1, 
                bordercolor=self.theme['button']['bd'], hovercolor=self.theme['button']['hover'],
                bg=self.theme['button']['bg'], fg=self.theme['button']['fg'],
                command=lambda e: command(**kwargs))
        button.bt.configure(font=self.theme['button']['font'], padx=3, pady=3)
        return button

    def browse_path(self):
        self.log_path.set(askopenfilename(filetypes=[('CombatLog files', '*.log'), ('All Files', '*.*')], 
                initialdir=os.getcwd()))

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_path, relative_path)
        return full_path

    def load_local_image(self, filename, width = None, height = None, forceAspect=False, copy=False):
        """Request image from web or fetch from local cache"""
        if os.path.exists(filename):
            image = Image.open(filename)
            if (width is not None and height is not None):
                if forceAspect: image = image.resize((width,height),Image.LANCZOS)
                else: image.thumbnail((width, height), resample=Image.LANCZOS)
            if not copy:
                return ImageTk.PhotoImage(image)
            else:
                return (ImageTk.PhotoImage(image), Image.open(filename))

    def resized_main_window(self, event):
        if '{}'.format(event.widget) == '.':
            self.main_window_last_change = event
            self.window.after(30, lambda value=event: self.resized_main_window_delay_check(value))
    
    def resized_main_window_delay_check(self, event):
        if self.main_window_last_change == event:
            self.windowWidth = event.width
            self.windowHeight = event.height
            self.resize_banner()

    def resize_banner(self):
        banner = self.banner2.copy()
        self.banner_height = int(self.windowWidth*(134/1920))
        self.banner = ImageTk.PhotoImage( banner.resize((self.windowWidth, self.banner_height)))
        self.bannerLabel.configure(image=self.banner)

    def initialize_ui(self):
        defaultFont = font.nametofont('TkDefaultFont')
        defaultFont.configure(family=self.theme['app']['font']['family'],size=self.theme['app']['font']['size'])

        self.bannerFrame = Frame(self.window, bg=self.theme['app']['bg'])
        self.bannerFrame.pack(fill=X)

        self.mainFrame = Frame(self.window, bg=self.theme['app']['bg'])
        self.mainFrame.pack(fill=BOTH, expand=True, padx=15, pady=(0,15))

        sidebarWrapper = Frame(self.mainFrame, bg=self.theme['app']['bg'])
        sidebarWrapper.grid(column=0, row=0, sticky='nsew')
        sidebarWrapper.pack_propagate(False)
        sidebarParter = Frame(sidebarWrapper, bg=self.theme['app']['oscr'], width=4)
        sidebarParter.pack(side=RIGHT, fill=Y, pady=15)
        self.sidebarFrame = Frame(sidebarWrapper, bg=self.theme['app']['bg'])
        self.sidebarFrame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
        self.sidebarFrame.columnconfigure(0, weight=1)
        self.sidebarFrame.columnconfigure(1, weight=0)


        self.contentFrame = Frame(self.mainFrame, bg=self.theme['app']['bg'])                   
        self.contentFrame.grid_propagate(False)
        #self.contentFrame.grid(column=1, row=0, sticky='nsew')
        self.contentFrame.columnconfigure(0, weight=1)
        self.contentFrame.columnconfigure(1, weight=0)
        self.contentFrame.rowconfigure(0, weight=0)
        self.contentFrame.rowconfigure(1, weight=1)      
        self.contentFrame.rowconfigure(2, weight=0)
        self.contentFrame.rowconfigure(3, weight=0)

        self.overview_table_frame = Frame(self.contentFrame, bg=self.theme['app']['bg'], highlightthickness=2, highlightbackground='#222222', highlightcolor='#222222')
        self.overview_table_frame.grid(row=2, column=0, sticky='new', padx=(30,30), pady=30, columnspan=2)
        self.overview_table_frame.columnconfigure(0, weight=1)
        self.overview_table_frame.columnconfigure(1, weight=0)
        self.overview_table_frame.rowconfigure(0, weight=0)
        self.overview_table_frame.rowconfigure(1, weight=0)

        self.mainFrame.columnconfigure(0, weight=1, uniform='main_col')
        self.mainFrame.columnconfigure(1, weight=4, uniform='main_col')
        self.mainFrame.columnconfigure(2, weight=0)
        self.mainFrame.rowconfigure(0, weight=1)

        self.banner_height = int(self.windowWidth*(134/1920))
        self.banner, self.banner2 = self.load_local_image(self.resource_path('local/oscrbanner.png'), self.windowWidth, 
                self.banner_height, copy=True)
        self.bannerLabel = Label(self.bannerFrame, image= self.banner, borderwidth=0, highlightthickness=0)
        self.bannerLabel.pack()

        self.initialize_splash()
        self.initialize_sidebar()
        self.initialize_main_notebook()

    def initialize_main_notebook(self):
        self.main_notebook = Frame(self.contentFrame, bg=self.theme['app']['bg'])
        self.main_notebook.grid(row=1, column=0, sticky='nsew', padx=30, pady=0)

        self.dps_bar_frame = Frame(self.main_notebook)
        self.dps_bar_frame.pack(fill=BOTH)
        self.dps_graph_frame = Frame(self.main_notebook)
        Label(self.dps_graph_frame, text='here am I').pack()
        self.dmg_graph_frame = Frame(self.main_notebook)

        buttonframe = Frame(self.contentFrame, bg=self.theme['app']['bg'])
        buttonframe.grid(row=0, column=0, sticky='n', pady=(35,0), padx=(0,45))

        dmg_button = self.create_default_button(buttonframe, 'Damage Graph',
                self.change_main_notebook_tab, new_tab=self.dmg_graph_frame)
        dps_graph_button = self.create_default_button(buttonframe, 'DPS Graph',
                self.change_main_notebook_tab, new_tab=self.dps_graph_frame)
        dps_button = self.create_default_button(buttonframe, 'DPS Bar',
                self.change_main_notebook_tab, new_tab=self.dps_bar_frame)

        dmg_button.pack(side=RIGHT, padx=4)
        dps_graph_button.pack(side=RIGHT, padx=4)
        dps_button.pack(side=RIGHT, padx=4)

    def initialize_sidebar(self):
        Label(self.sidebarFrame, text='CombatLog Filepath', **self.theme['label']).grid(
                row=0, column=0, sticky='w', pady=(10,0))
        self.log_path = StringVar(self.window, value=self.settings['log_path'])
        self.log_path.trace_add('write', lambda e1, e2, e3: self.set_setting('log_path', self.log_path.get()))
        self.entry_path = Entry(self.sidebarFrame, **self.theme['entry'], textvariable=self.log_path)
        self.entry_path.grid(row=1, column=0, sticky='ew', pady=5)
        button_frame = Frame(self.sidebarFrame, bg=self.theme['app']['bg'])
        button_frame.grid(row=2, column=0, sticky='ew', pady=(0,10))
        button_frame.columnconfigure(0, weight=0)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=0)
        browse_button = self.create_default_button(button_frame, text='Browse...', command=self.browse_path)
        browse_button.grid(row=0, column=0, sticky='w', padx=(0,8))
        analyze_button = self.create_default_button(button_frame, text='Analyze', command=self.analyze_log)
        analyze_button.grid(row=0, column=1, sticky='ew')
        log_selector_frame = Frame(self.sidebarFrame, bg=self.theme['app']['light_bg'], height=300)
        log_selector_frame.grid(row=3, column=0, pady=35, sticky='ew')

        combat_analysis_bt = self.create_default_button(self.sidebarFrame, text='Combat Analysis', 
                command=self.open_combat_analysis)
        combat_analysis_bt.grid(row=4, column=0, sticky='w')

    def change_main_notebook_tab(self, new_tab:Frame):
        if new_tab.winfo_ismapped(): 
            return
        for child in self.main_notebook.winfo_children():
            if child.winfo_ismapped():
                child.pack_forget()
                new_tab.pack(fill=BOTH)
    
    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def blur(self, event):
        if not event.widget == self.entry_path:
            self.window.focus()

    def initialize_splash(self):
        self.in_splash = False
        self.splash_frame = Frame(self.mainFrame, bg=self.theme['app']['bg'], highlightthickness=0)
        Label(self.splash_frame, text='Loading...', fg=self.theme['app']['oscr'], background=self.theme['app']['bg'],
                font=(self.theme['app']['font']['family'], 18, 'bold')).place(relx=0.5, rely=0.5, anchor=CENTER)
        
    def make_splash(self):
        self.in_splash = True
        self.contentFrame.grid_forget()
        self.splash_frame.grid(row=0, column=1, sticky='nsew')
        
        
    def terminate_splash(self):
        self.splash_frame.grid_forget()
        self.contentFrame.grid(column=1, row=0, sticky='nsew')
        self.in_splash = False

    def clear_frame(self, fr):
        for w in fr.winfo_children():
            w.destroy()

    def initialize_backend(self):
        self.overviewData = [[],[],[]]  # [[data], [headers], [indexes]]
        self.players = {}
        self.load_settings()

    def save_settings(self):
        with open('local/oscr_settings.json', 'w') as f:
            json.dump(self.settings, f)

    def load_settings(self):
        if os.path.exists('local/oscr_settings.json'):
            with open('local/oscr_settings.json') as f:
                new_settings = json.load(f)
            self.settings.update(new_settings)
        
    def initialize_window(self):
        self.window = Tk()
        self.window.iconphoto(False, PhotoImage(file=self.resource_path('local/oscr_icon_small.png')))
        self.window.title('Open-Source Combatlog Reader')
        self.window.geometry('1000x1000')
        self.window.configure(background=self.theme['app']['oscr'])
        self.window.bind('<Configure>', self.resized_main_window)
        self.window.bind_all('<Button-1>', lambda e: self.blur(e))
        self.window.update()
        self.windowWidth = self.window.winfo_width()
        self.windowHeight = self.window.winfo_height()
        self.window.protocol("WM_DELETE_WINDOW", lambda:quit())

    def __init__(self) -> None:
        self.initialize_window()
        self.initialize_backend()
        self.initialize_ui()
       
        #self.get_data()
        #self.plot_test()
        #self.create_overview()

    def run(self):
        if __name__ == '__main__':
            self.window.mainloop()


class PlainButton(Frame):
    def __init__(self, master, text:str = '', bg:str = 'grey', fg:str = '#000000', hovercolor:str = '#ffffff', 
                bordercolor:str = '#000000', command = None, *args, **kwargs):
        super().__init__(master, highlightbackground=bordercolor, *args, **kwargs)
        self.bt = Label(self, text=text, bg=bg, fg=fg)
        self.bt.pack(fill=BOTH, padx=0, pady=0)
        self.hovercolor = hovercolor
        self.bordercolor = bordercolor

        for w in [self, self.bt]:
            w.bind('<Enter>', self.on_enter)
            w.bind('<Leave>', self.on_leave)
            w.bind('<Button-1>', command)

    def on_enter(self, event):
        self.configure(highlightbackground=self.hovercolor)

    def on_leave(self, event):
        self.configure(highlightbackground=self.bordercolor)



OSCRUI().run()