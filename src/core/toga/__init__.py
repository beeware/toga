from .app import App, DocumentApp, MainWindow
# Resources
from .colors import hsl, hsla, rgb, rgba
from .command import GROUP_BREAK, SECTION_BREAK, Command, CommandSet, Group
from .documents import Document
from .fonts import Font
from .icons import Icon
from .images import Image
from .keys import Key
from .widgets.activityindicator import ActivityIndicator
# Widgets
from .widgets.base import Widget
from .widgets.box import Box
from .widgets.button import Button
from .widgets.canvas import Canvas
from .widgets.datepicker import DatePicker
from .widgets.detailedlist import DetailedList
from .widgets.divider import Divider
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
from .widgets.textinput import TextInput
from .widgets.timepicker import TimePicker
from .widgets.tree import Tree
from .widgets.webview import WebView
from .window import Window

__all__ = [
    # Applications
    'App', 'DocumentApp', 'MainWindow',
    # Commands
    'Command', 'CommandSet', 'Group', 'GROUP_BREAK', 'SECTION_BREAK',
    # Documents
    'Document',
    # Keys
    'Key',

    # Resources
    'hsl', 'hsla', 'rgb', 'rgba',  # Colors
    'Font',
    'Icon',
    'Image',

    # Widgets
    'ActivityIndicator',
    'Box',
    'Button',
    'Canvas',
    'DetailedList',
    'Divider',
    'Window',
    'Widget',
    'ImageView',
    'Label',
    'DatePicker',
    'TimePicker',
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
    'WebView'
]

# Examples of valid version strings
# __version__ = '1.2.3.dev1'  # Development release 1
# __version__ = '1.2.3a1'     # Alpha Release 1
# __version__ = '1.2.3b1'     # Beta Release 1
# __version__ = '1.2.3rc1'    # RC Release 1
# __version__ = '1.2.3'       # Final Release
# __version__ = '1.2.3.post1' # Post Release 1

__version__ = '0.3.0.dev30'
