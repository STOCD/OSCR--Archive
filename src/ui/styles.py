import copy
from PyQt6.QtGui import QFont  

weight_conversion = {
        'normal': QFont.Weight.Normal,
        'bold': QFont.Weight.Bold,
        'extrabold': QFont.Weight.ExtraBold,
        'medium': QFont.Weight.Medium
    }

def get_style(self, widget, override={}):
    if widget is None or widget == '':
        return get_css(self, override)
    elif widget != 'app' and widget != 'defaults' and widget in self.theme.keys():
        if len(override) > 0:
            style = merge_style(self, self.theme[widget], override)
        else:
            style = self.theme[widget]
        return get_css(self, style)

def merge_style(self, s1:dict, s2:dict):
    """
    Returns new dictionary where the given styles are merged.
    Up to one sub-dictionary is merged recursively.

    Parameters:
    - :param s1: Style-dict 1
    - :param s2: Style-dict 2
    """
    result = copy.deepcopy(s1)
    for k, v in s2.items():
        if k in result.keys() and isinstance(result[k], dict) and isinstance(v, dict):
            result[k].update(v)
            continue
        result[k] = v
    return result

def get_css(self, style:dict):
    css = ''
    for key, val in style.items():
        if key == 'font' or key == 'hover':
            continue
        elif isinstance(val, int):
            css += f'{key}:{val}px;'
        else:
            css += f'{key}:{val};'
    return css

def get_style_class(self, class_name:str, widget, override={}):
    if widget is None or widget == '':
        style = override
    elif widget != 'app' and widget != 'defaults' and widget in self.theme.keys():
        if len(override) > 0:
            style = merge_style(self, self.theme[widget], override)
        else:
            style = self.theme[widget]
    else:
        raise KeyError(f'Parameter widget=`{widget}` must be None or key of self.theme '
                'except `app` or `defaults`.')
    main = f'{class_name} {{{get_css(self, style)}}}'
    if 'hover' in style:
        main += f''' {class_name}:hover {{{get_css(self, style['hover'])}}}'''
    return main

def theme_font(self, key, font_spec:tuple=()):
    if len(font_spec) != 3:
        try:
            font = self.theme[key]['font']
        except KeyError:
            font = self.theme['app']['font']
    else:
        font = font_spec
    font_family = (font[0], *self.theme['app']['font-fallback'])
    try:
        font_weight = weight_conversion[font[2]]
    except KeyError:
        font_weight = QFont.Weight.Normal
    return QFont(font_family, font[1], font_weight)

