from PyQt6.QtWidgets import QWidget, QSizePolicy, QPushButton, QFrame, QLabel
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import QRect
from types import FunctionType, BuiltinFunctionType, MethodType

FUNC = (FunctionType, BuiltinFunctionType, MethodType)

class WidgetBuilder():

    from src.ui.styles import get_style_class, get_style, merge_style, theme_font

    def __init__(self) -> None:
        """
        This class is not inteded to be instantiated.
        """
        return

    def create_button(self, text, style:str='', parent=None, style_override={}):
        """
        Creates a button according to style with parent.

        Parameters:
        - :param text: text to be shown on the button
        - :param style: name of the style as in self.theme or style dict
        - :param parent: parent of the button (optional)
        - :param style_override: style dict to override default style (optional)

        :return: configured QPushButton
        """
        button = QPushButton(text, parent)
        button.setStyleSheet(self.get_style_class('QPushButton', style, style_override))
        if 'font' in style_override.keys():
            button.setFont(self.theme_font(style, style_override['font']))
        else:
            button.setFont(self.theme_font(style))
        return button

    def create_frame(self, parent, style='frame', style_override={}):
        """
        Creates a frame with default styling and parent

        Parameters:
        - :param parent: parent of the frame (optional)
        - :param style: style dict to override default style (optional)

        :return: configured QFrame
        """
        frame = QFrame(parent)
        frame.setStyleSheet(self.get_style(style, style_override))
        return frame

    def create_label(self, text, style:str='', parent=None, style_override={}):
        """
        Creates a label according to style with parent.

        Parameters:
        - :param text: text to be shown on the label
        - :param style: name of the style as in self.theme
        - :param parent: parent of the label (optional)
        - :param style_override: style dict to override default style (optional)

        :return: configured QLabel
        """
        label = QLabel(parent)
        label.setText(text)
        label.setStyleSheet(self.get_style(style, style_override))
        if 'font' in style_override.keys():
            label.setFont(self.theme_font(style, style_override['font']))
        else:
            label.setFont(self.theme_font(style))
        return label
        
    def create_button_series(self, parent, buttons:dict, style, shape:str='row', seperator:str=''):
        """
        Creates a row / column of buttons.

        Parameters:
        - :param parent: widget that will contain the buttons
        - :param buttons: dictionary containing button details
        - :param style: key for self.theme -> default style
        - :param shape: row / column
        - :param seperator: string seperator displayed between buttons (optional)

        :return: populated QVBoxlayout / QHBoxlayout
        """
        if 'default' in buttons.keys():
            defaults = self.merge_style(self.theme[style], buttons.pop('default'))
        else:
            defaults = self.theme[style]

        if shape == 'column':
            layout = QVBoxLayout()
        else:
            shape = 'row'
            layout = QHBoxLayout()
    	
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        if seperator != '':
            sep_style = {'color':defaults['color'],'margin':0, 'padding':0, 'background':'rgba(0,0,0,0)'}
        
        for i, (name, detail) in enumerate(buttons.items()):
            if 'style' in detail.keys():
                button_style = self.merge_style(defaults, detail['style'])
            else:
                button_style = defaults
            bt = self.create_button(name, style, parent, button_style)
            if 'callback' in detail and isinstance(detail['callback'], FUNC):
                bt.clicked.connect(detail['callback'])
            layout.addWidget(bt)
            if seperator != '' and i < (len(buttons) - 1):
                sep_label = self.create_label(seperator, 'label', parent, sep_style)
                layout.addWidget(sep_label)
        
        return layout
            

class BannerLabel(QWidget):
    def __init__(self, path, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setPixmap(QPixmap(path))
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    def setPixmap(self, p):
        self.p = p
        self.update()

    def paintEvent(self, event):
        if not self.p.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            w = self.rect().width()
            h = w * 126/2880
            rect = QRect(0, 0, w, h)
            painter.drawPixmap(rect, self.p)
            self.setMaximumHeight(h)
