from java import jclass

from .label import LabelProbe


# On Android, a TextInput is just an editable TextView
class TextInputProbe(LabelProbe):
    native_class = jclass("android.widget.EditText")
