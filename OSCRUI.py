import tkinter
import statistics
from tkinter import ttk
from tkinter import Tk
from tkinter import PhotoImage, font
from tkinter import Frame, Label, Button
from tkinter import BOTH, BOTTOM, DISABLED, END, FLAT, HORIZONTAL
from tkinter import LEFT, NORMAL, RIGHT, TOP, VERTICAL, WORD, X, Y
import sys
import os
import PIL
from PIL import Image, ImageTk, ImageGrab
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Easytable import Easytable

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
            'accent': '#c82934' #b81924
        },
        'bar':{
            'font':{
                'weight': 'bold',
                'size': 13
            },
            'fg': '#888888',
            'bg': '#424242',
            'light_text':'#d0d0d0',
            'dark_text': '#222222'
        },
        'scroll':{
            'trough':{'troughcolor':'#424242','troughrelief':'flat','borderwidth':0},
            'arrow':{'background':'#888888', 'relief':'flat', 'borderwidth':0, 'arrowcolor':'#3a3a3a'},
            'thumb':{'relief':'flat', 'background':'#888888', 'borderwidth':0}
        },
        'table':{
            'heading':{'font':('Helvetica',17,'normal'), 'fg':'#b3b3b3', 'bg':'#3a3a3a'},
            'content':{'bg':'#424242', 'fg':'#ffffff', 'font':('Helvetica',14,'bold'), 'anchor':'e'},
            'bordercolor': '#000000',
            'borderwidth':{'top_border':0, 'bottom_border':1, 'left_border':0, 'right_border':1}
        }
    }

    overviewData = []
    overviewTableHeaders = []

    def get_data(self):
        data = OSCR.main()
        self.overviewData = data[1:]
        self.overviewTableHeaders = data[:1][0]
        print("---------")
        print(self.overviewTableHeaders)

    def initialize_styles(self):
        self.style = ttk.Style()
        self.style.configure('oscr_overview.Treeview', highlightthickness=0, bd=0, font=('Helvetica', 13, 'normal'))
        #self.style.theme_use('default')

    def create_treeview(self, data):
        pass

    def test_treeview(self):
        tree_frame = Frame(self.contentFrame, bg='black')
        tree_frame.grid(row=2, column=0, sticky='new', padx=(100,30), pady=30, columnspan=2)
        table = Easytable(tree_frame, columns=self.overviewTableHeaders, border_color=self.theme['table']['bordercolor'], heading_style=self.theme['table']['heading'], scrollbar_style=self.theme['scroll'])
        for data in self.overviewData:
            table._add_row(row_data=self.data_round(data))
        table.configure_style('content', self.theme['table']['content'])
        table.configure_borders('heading content', **self.theme['table']['borderwidth'])
        table._set_height(5)
        table.pack(fill=X)

    def data_round(self, li:list):
        new_li = list()
        for el in li:
            if isinstance(el, (int, float)):
                new_li.append(f'{round(el,2):,}')
            else:
                new_li.append(el)
        return new_li

    def plot_test(self):
        dps = [el[2] for el in self.overviewData]
        x = [el[0] for el in self.overviewData]
        lbs = self.format_bar_labels(dps)
        with plt.style.context(self.resource_path('local/oscr_default.mplstyle')):
            f, a = plt.subplots()
            bars = [a.barh(x[j], dps[j], color=self.theme['bar']['fg']) for j in range(len(dps))]
            for i, bar in enumerate(bars):
                self.create_bar_label(bar, a, dps, dps[i], lbs[i], i)
            f.set_figwidth(int(self.windowWidth*0.075))
        plt.tight_layout()
        chart = FigureCanvasTkAgg(f, self.contentFrame).get_tk_widget()
        chart.grid(row=1, column=0, padx=15, pady=15, sticky='e', columnspan=2)

    def create_bar_label(self, bar, axis: Axes , data, current, label, n):
        if current > max(data)/10:
            color = self.theme['bar']['dark_text']
            
            #axis.bar_label(bar, labels=[label], label_type='center', fontweight='bold', fontsize=13, color=color, padding=5)

            axis.text(max(data)/100,n-.08,label,color=color, fontweight=self.theme['bar']['font']['weight'], fontsize=self.theme['bar']['font']['size'])

        else:
            color = self.theme['bar']['light_text']
            axis.bar_label(bar, labels=[label], label_type='edge', fontweight=self.theme['bar']['font']['weight'], fontsize=self.theme['bar']['font']['size'], color=color, padding=5)
        
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
            if(width is not None and height is not None):
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
        self.banner = ImageTk.PhotoImage( banner.resize((self.windowWidth, int(self.windowWidth*(134/1920)))))
        self.bannerLabel.configure(image=self.banner)

    def initialize_ui(self):
        defaultFont = font.nametofont('TkDefaultFont')
        defaultFont.configure(family=self.theme['app']['font']['family'],size=self.theme['app']['font']['size'])

        self.bannerFrame = Frame(self.window, bg=self.theme['app']['bg'])
        self.bannerFrame.pack(fill=X)

        self.mainFrame = Frame(self.window, bg=self.theme['app']['bg'])
        self.mainFrame.pack(fill=BOTH, expand=True, padx=15, pady=(0,15))

        self.sidebarFrame = Frame(self.mainFrame, bg=self.theme['app']['bg'])
        self.sidebarFrame.grid(column=0, row=0, sticky='nsew')

        self.contentFrame = Frame(self.mainFrame, bg=self.theme['app']['bg'])
        self.contentFrame.grid(column=1, row=0, sticky='nsew')
        self.contentFrame.columnconfigure(0, weight=1)
        self.contentFrame.columnconfigure(1, weight=1)
        self.contentFrame.columnconfigure(2, weight=0)  
        self.contentFrame.rowconfigure(0, weight=0)
        self.contentFrame.rowconfigure(1, weight=0)      
        self.contentFrame.rowconfigure(2, weight=1)
        self.contentFrame.rowconfigure(3, weight=0)      


        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.columnconfigure(1, weight=5)
        self.mainFrame.columnconfigure(2, weight=0)
        self.mainFrame.rowconfigure(0, weight=1)

        self.banner, self.banner2 = self.load_local_image(self.resource_path('local/oscrbanner.png'), self.windowWidth, 134, copy=True)
        self.bannerLabel = Label(self.bannerFrame, image= self.banner, borderwidth=0, highlightthickness=0)
        self.bannerLabel.pack()

        Button(self.sidebarFrame, text="click me I'm doing nothing!").pack()
        Button(self.contentFrame, text="click me I'm doing nothing!").grid(row=0, column=0, sticky='e', columnspan=2)



    def initialize_window(self):
        self.window = Tk()
        self.window.iconphoto(False, PhotoImage(file=self.resource_path('local/oscr_icon_small.png')))
        self.window.title('Open-Source Combatlog Reader')
        self.window.configure(background=self.theme['app']['accent'])
        self.window.bind('<Configure>', self.resized_main_window)
        self.windowWidth = self.window.winfo_width()
        self.windowHeight = self.window.winfo_height()
        self.window.protocol("WM_DELETE_WINDOW", lambda:quit())

    def __init__(self) -> None:
        self.initialize_window()
        self.initialize_ui()
        self.initialize_styles()
        self.get_data()
        self.plot_test()
        self.test_treeview()

    def run(self):
        if __name__ == '__main__':
            self.window.mainloop()

OSCRUI().run()