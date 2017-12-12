from . import django
from .app import *
from .widgets.box import *
from .widgets.button import *
from .widgets.label import *
from .widgets.textinput import *
from .widgets.webview import *
from .window import *


__all__ = [
    '__version__',
    'django',
    'App',
    'Window', 'MainWindow',
    'Box',
    'Button',
    'Label',
    'TextInput',
    'WebView',
]

# Examples of valid version strings
# __version__ = '1.2.3.dev1'  # Development release 1
# __version__ = '1.2.3a1'     # Alpha Release 1
# __version__ = '1.2.3b1'     # Beta Release 1
# __version__ = '1.2.3rc1'    # RC Release 1
# __version__ = '1.2.3'       # Final Release
# __version__ = '1.2.3.post1' # Post Release 1

__version__ = '0.3.0.dev1'
