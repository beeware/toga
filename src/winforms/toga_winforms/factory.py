from .app import App, MainWindow
from .command import Command

# from resources.colors import ...
# from resources.fonts import font
from .resources.icons import Icon
from .resources.images import Image

from .widgets.box import Box
from .widgets.button import Button
# from .widgets.canvas import Canvas
# from .widgets.detailedlist import DetailedList
from .widgets.imageview import *
from .widgets.label import *
from .widgets.multilinetextinput import *
from .widgets.numberinput import NumberInput
from .widgets.optioncontainer import *
from .widgets.passwordinput import *
from .widgets.progressbar import *
from .widgets.scrollcontainer import *
from .widgets.selection import Selection
from .widgets.slider import *
from .widgets.splitcontainer import *
from .widgets.switch import *
from .widgets.table import *
from .widgets.webview import *
from .window import Window


def not_implemented(feature):
    print('[Winforms] Not implemented: {}'.format(feature))


__all__ = [
    'not_implemented',

    'App', 'MainWindow',
    'Command',

    # Resources
    # 'color',
    # 'font',
    'Icon',
    'Image',

    # Widgets
    'Box',
    'Button',
    # 'Canvas',
    # 'DetailedList',
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
    # 'Tree',
    'WebView',
    'Window',
]
