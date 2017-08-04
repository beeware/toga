from .app import *
from .command import *
from .window import Window
from .constants import *

# Font support
from .font import Font

# Widgets
from .widgets.base import Layout, Point, Widget

from .widgets.box import Box
from .widgets.button import Button
# from .widgets.icon import Icon
from .widgets.image import *
from .widgets.imageview import *
from .widgets.label import Label
from .widgets.multilinetextinput import *
from .widgets.optioncontainer import *
from .widgets.passwordinput import *
from .widgets.progressbar import *
from .widgets.scrollcontainer import *
from .widgets.slider import *
from .widgets.splitcontainer import *
from .widgets.switch import *
from .widgets.table import *
from .widgets.textinput import TextInput

from .widgets.tree import *
from .widgets.webview import *
from .widgets.selection import Selection
from .widgets.numberinput import NumberInput

__all__ = [
    'App', 'MainWindow',
    'constants',
    'Command', 'Group', 'GROUP_BREAK', 'SECTION_BREAK',
    'Window',
    'Font',
    'Widget'
    'Box',
    'Button',
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

__version__ = '0.2.13.dev1'
