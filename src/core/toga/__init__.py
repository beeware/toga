from .app import *
from .command import *
from .constants import *
from .color import hsl, hsla, rgb, rgba
from .font import Font

# Widgets
from .widgets.base import Widget

from .widgets.box import Box
from .widgets.button import Button
from .widgets.canvas import Canvas
from .widgets.detailedlist import DetailedList
from .widgets.image import *
from .widgets.imageview import *
from .widgets.label import Label
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
from .widgets.textinput import TextInput
from .widgets.tree import *
from .widgets.webview import *
from .window import Window


__all__ = [
    # Applications
    'App', 'MainWindow',
    # Colors
    'hsv', 'hsva', 'rgb', 'rgba',
    # Commands
    'Command', 'Group', 'GROUP_BREAK', 'SECTION_BREAK',
    # Fonts
    'Font',

    # Widgets
    'DetailedList'
    'Window',
    'Widget'
    'Box',
    'Button',
    'Canvas',
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
]

# Examples of valid version strings
# __version__ = '1.2.3.dev1'  # Development release 1
# __version__ = '1.2.3a1'     # Alpha Release 1
# __version__ = '1.2.3b1'     # Beta Release 1
# __version__ = '1.2.3rc1'    # RC Release 1
# __version__ = '1.2.3'       # Final Release
# __version__ = '1.2.3.post1' # Post Release 1

__version__ = '0.3.0.dev8'

