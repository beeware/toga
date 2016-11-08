# Django app definition
from . import django

# Core capabilities
from .app import *
from .window import *
# from .command import *

# Widgets
from .widgets.box import *
from .widgets.button import *
# from .widgets.icon import *
# from .widgets.image import *
# from .widgets.imageview import *
# from .widgets.label import *
# from .widgets.list import *
# from .widgets.dialog import *
# from .widgets.multilinetextinput import *
# from .widgets.optioncontainer import *
# from .widgets.passwordinput import *
# from .widgets.progressbar import *
# from .widgets.scrollcontainer import *
# from .widgets.splitcontainer import *
# from .widgets.table import *
# from .widgets.textinput import *
# from .widgets.tree import *
# from .widgets.webview import *

__all__ = [
    '__version__',
    'django',
    'App',
    'Window', 'MainWindow',
#     'Command', 'SEPARATOR', 'SPACER', 'EXPANDING_SPACER',
    'Box',
    'Button',
#     'Icon', 'TIBERIUS_ICON',
#     'Image',
#     'ImageView',
#     'Label',
    # 'List', 'SimpleListElement',
#     'Dialog',
#     'MultilineTextInput',
#     'OptionContainer',
#     'PasswordInput',
#     'ProgressBar',
#     'ScrollContainer',
#     'SplitContainer',
#     'Table',
    # 'TextInput',
#     'Tree',
#     'WebView',
]

# Examples of valid version strings
# __version__ = '1.2.3.dev1'  # Development release 1
# __version__ = '1.2.3a1'     # Alpha Release 1
# __version__ = '1.2.3b1'     # Beta Release 1
# __version__ = '1.2.3rc1'    # RC Release 1
# __version__ = '1.2.3'       # Final Release
# __version__ = '1.2.3.post1' # Post Release 1

__version__ = '0.2.4'
