from .app import App, DocumentApp, MainWindow
from .command import Command
from .documents import Document
from .fonts import Font
from .icons import Icon
from .images import Image
from .paths import paths
from . import dialogs

from .widgets.activityindicator import ActivityIndicator
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
from .widgets.navigationview import NavigationView
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


def not_implemented(feature):
    raise NotImplementedError()


__all__ = [
    'not_implemented',

    'App', 'DocumentApp', 'MainWindow',
    'Command',
    'Document',

    'Font',
    'Icon',
    'Image',
    'paths',
    'dialogs',

    'ActivityIndicator',
    'Box',
    'Button',
    'Canvas',
    'DetailedList',
    'Divider',
    'ImageView',
    'DatePicker',
    'TimePicker',
    'Label',
    'MultilineTextInput',
    'NavigationView',
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

    # Widget is also required for testing purposes
    # Real backends shouldn't expose Widget.
    'Widget'
]
