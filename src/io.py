import os
import sys
import re
from PyQt6.QtGui import QIcon, QPixmap

def get_asset_path(self, asset_name) -> str:
    """
    returns the absolute path to a file in the asset folder
    """
    fp = os.path.join(self.app_dir, 'assets', asset_name)
    if os.path.exists(fp):
        return fp
    else:
        return ''

def load_icon(self, path, h=None) -> QIcon:
    """
    Loads icon from path and returns it.

    Parameters:
    - :param path: path to icon
    - :param h: height to which the icon should be scaled
    """
    pm = QPixmap(get_asset_path(self, path))
    if isinstance(h, int):
        pm.scaledToHeight(h)
    return QIcon(pm)

def sanitize_file_name(self, txt, chr_set='extended') -> str:
    """Converts txt to a valid filename.

    Parameters:
    - :param txt: The path to convert.
    - :param chr_set: 
        - 'printable':    Any printable character except those disallowed on Windows/*nix.
        - 'extended':     'printable' + extended ASCII character codes 128-255
        - 'universal':    For almost *any* file system.
    """
    FILLER = '-'
    MAX_LEN = 255  # Maximum length of filename is 255 bytes in Windows and some *nix flavors.

    # Step 1: Remove excluded characters.
    BLACK_LIST = set(chr(127) + r'<>:"/\|?*')
    white_lists = {
        'universal': {'-.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'},
        'printable': {chr(x) for x in range(32, 127)} - BLACK_LIST,     # 0-32, 127 are unprintable,
        'extended' : {chr(x) for x in range(32, 256)} - BLACK_LIST,
    }
    white_list = white_lists[chr_set]
    result = ''.join(x if x in white_list else FILLER for x in txt)

    # Step 2: Device names, '.', and '..' are invalid filenames in Windows.
    DEVICE_NAMES = 'CON,PRN,AUX,NUL,COM1,COM2,COM3,COM4,' \
                    'COM5,COM6,COM7,COM8,COM9,LPT1,LPT2,' \
                    'LPT3,LPT4,LPT5,LPT6,LPT7,LPT8,LPT9,' \
                    'CONIN$,CONOUT$,..,.'.split()  # This list is an O(n) operation.
    DEVICE_NAMES = ('CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9', 'CONIN$', 'CONOUT$', '..', '.')
    if '.' in txt:
        name, _, ext = result.rpartition('.')
        ext = f'.{ext}'
    else:
        name = result
        ext = ''
    if name in DEVICE_NAMES:
        result = f'-{result}-{ext}'

    # Step 3: Truncate long files while preserving the file extension.
    if len(result) > MAX_LEN:
        result = result[:MAX_LEN - len(ext)] + ext

    # Step 4: Windows does not allow filenames to end with '.' or ' ' or begin with ' '.
    result = re.sub(r"[. ]$", FILLER, result)
    result = re.sub(r"^ ", FILLER, result)

    return result