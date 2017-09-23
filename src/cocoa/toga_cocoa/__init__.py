# Core capabilities
from .app import *
from .command import Group, Command
from .window import *

# Font support
from .font import Font

# Widgets
from .widgets.box import *
from .widgets.button import *
from .widgets.detailedlist import *
from .widgets.icon import *
from .widgets.image import *
from .widgets.imageview import *
from .widgets.label import *
from .widgets.multilinetextinput import *
from .widgets.optioncontainer import *
from .widgets.passwordinput import *
from .widgets.progressbar import *
from .widgets.scrollcontainer import *
from .widgets.slider import *
from .widgets.splitcontainer import *
from .widgets.switch import *
from .widgets.table import *
from .widgets.textinput import *
from .widgets.tree import *
from .widgets.webview import *
from .widgets.selection import Selection
from .widgets.numberinput import NumberInput

__all__ = [
    '__version__',
    'App', 'MainWindow',
    'Group', 'Command',
    'Window',
    'Box',
    'Button',
    'DetailedList',
    'Icon', 'TIBERIUS_ICON',
    'Image',
    'ImageView',
    'Font',
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

__version__ = '0.2.15'
