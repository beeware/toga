from .app import App, MainWindow
from .command import Command
# from .font import font
from .widgets.box import Box
from .widgets.button import Button
# from .widgets.canvas import Canvas
# from .widgets.detailedlist import DetailedList
from .widgets.icon import Icon
from .widgets.image import Image
from .widgets.imageview import ImageView
from .widgets.label import Label
from .widgets.multilinetextinput import MultilineTextInput
from .widgets.numberinput import NumberInput
from .widgets.optioncontainer import OptionContainer
from .widgets.passwordinput import PasswordInput
from .widgets.progressbar import ProgressBar
from .widgets.scrollcontainer import ScrollContainer
from .widgets.selection import Selection
from .widgets.slider import Slider
from .widgets.splitcontainer import SplitContainer
from .widgets.switch import Switch
from .widgets.table import Table
from .widgets.tree import Tree
from .widgets.webview import WebView
from .window import Window


def not_implemented(feature):
    print('[Winforms] Not implemented: {}'.format(feature))


__all__ = [
    'not_implemented',

    'App', 'MainWindow',
    # 'color',
    'Command',
    # 'font',
    'Box',
    'Button',
    # 'Canvas',
    # 'DetailedList',
    'Icon',
    'Image',
    'ImageView',
    'Label',
    'MultilineTextInput',
    'NumberInput',
    'OptionContainer',
    'PasswordInput',
    'ProgressBar',
    'ScrollContainer',
    'Selection',
    'Slider',
    'SplitContainer',
    'Switch',
    'Table',
    'TextInput',
    'Tree',
    'WebView',
    'Window',
]
