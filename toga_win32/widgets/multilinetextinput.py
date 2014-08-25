from .textinput import TextInput
from ..libs import *

class MultilineTextInput(TextInput):
    control_style = ES_MULTILINE | ES_WANTRETURN | ES_AUTOVSCROLL