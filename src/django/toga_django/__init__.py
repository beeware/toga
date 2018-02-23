from . import django
from .app import App, MainWindow
# from .color import color
# from .command import Command
# from .font import font
from .widgets.box import *
from .widgets.button import *
# from .widgets.canvas import Canvas
# from .widgets.detailedlist import DetailedList
# from .widgets.icon import *
# from .widgets.image import *
# from .widgets.imageview import *
from .widgets.label import *
# from .widgets.multilinetextinput import *
# from .widgets.numberinput import NumberInput
# from .widgets.optioncontainer import *
# from .widgets.passwordinput import *
# from .widgets.progressbar import *
# from .widgets.scrollcontainer import *
# from .widgets.selection import Selection
# from .widgets.slider import *
# from .widgets.splitcontainer import *
# from .widgets.switch import *
# from .widgets.table import *
from .widgets.textinput import *
# from .widgets.tree import *
from .widgets.webview import *
from .window import Window


__all__ = [
    '__version__',
    'django',
    'App', 'MainWindow',
    # 'color',
    # 'Command',
    # 'font',
    'Box',
    'Button',
    # 'Canvas',
    # 'DetailedList',
    # 'Icon',
    # 'Image',
    # 'ImageView',
    'Label',
    # 'MultilineTextInput',
    # 'NumberInput',
    # 'OptionContainer',
    # 'PasswordInput',
    # 'ProgressBar',
    # 'ScrollContainer',
    # 'Selection',
    # 'Slider',
    # 'SplitContainer',
    # 'Switch',
    # 'Table',
    'TextInput',
    # 'Tree',
    'WebView',
    'Window',
]

# Examples of valid version strings
# __version__ = '1.2.3.dev1'  # Development release 1
# __version__ = '1.2.3a1'     # Alpha Release 1
# __version__ = '1.2.3b1'     # Beta Release 1
# __version__ = '1.2.3rc1'    # RC Release 1
# __version__ = '1.2.3'       # Final Release
# __version__ = '1.2.3.post1' # Post Release 1

__version__ = '0.3.0.dev8'
