from .app import App, MainWindow
from .colors import native_color
from .fonts import Font
from .icons import Icon
from .images import Image
from .paths import paths
from . import dialogs

from .widgets.box import Box
from .widgets.button import Button
from .widgets.canvas import Canvas
from .widgets.detailedlist import DetailedList
from .widgets.imageview import ImageView
from .widgets.label import Label
from .widgets.multilinetextinput import MultilineTextInput
from .widgets.numberinput import NumberInput
# from .widgets.optioncontainer import OptionContainer
from .widgets.passwordinput import PasswordInput
from .widgets.progressbar import ProgressBar
from .widgets.scrollcontainer import ScrollContainer
from .widgets.selection import Selection
from .widgets.slider import Slider
# from .widgets.splitcontainer import SplitContainer
from .widgets.switch import Switch
# from .widgets.table import Table
from .widgets.textinput import TextInput
# from .widgets.tree import Tree
from .widgets.webview import WebView
from .window import Window

# from .command import Command


def not_implemented(feature):
    print('[iOS] Not implemented: {}'.format(feature))


__all__ = [
    'not_implemented',

    'App', 'MainWindow',
    # 'Command',

    # Resources
    'native_color',  # colors
    'Font',
    'Icon',
    'Image',
    'paths',
    "dialogs",

    # Widgets
    'Box',
    'Button',
    'Canvas',
    'DetailedList',
    'ImageView',
    'Label',
    'MultilineTextInput',
    'NumberInput',
    # 'OptionContainer',
    'PasswordInput',
    'ProgressBar',
    'ScrollContainer',
    'Selection',
    'Slider',
    # 'SplitContainer',
    'Switch',
    # 'Table',
    'TextInput',
    # 'Tree',
    'WebView',
    'Window',
]
