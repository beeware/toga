from .app import App, MainWindow
# from .command import Command


from .resources.colors import native_color
from .resources.fonts import Font
from .resources.icons import Icon
from .resources.images import Image

from .widgets.box import Box
from .widgets.button import Button
# from .widgets.canvas import Canvas
from .widgets.detailedlist import DetailedList
from .widgets.imageview import *
from .widgets.label import Label
from .widgets.multilinetextinput import *
from .widgets.numberinput import NumberInput
# from .widgets.optioncontainer import *
from .widgets.passwordinput import *
from .widgets.progressbar import *
from .widgets.scrollcontainer import *
from .widgets.selection import Selection
from .widgets.slider import *
# from .widgets.splitcontainer import *
from .widgets.switch import *
# from .widgets.table import *
from .widgets.textinput import TextInput
# from .widgets.tree import *
from .widgets.webview import *
from .window import Window


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

    # Widgets
    'Box',
    'Button',
    # 'Canvas',
    'DetailedList',
    'ImageView',
    'Label',
    'MultilineTextInput',
    'NumberInput',
    # 'OptionContainer',
    'PasswordInput',
    'ProgressBar',
    # 'ScrollContainer',
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
