# from android.widget import EditText
#
# from ..app import App
# from .base import Widget
#
#
# class TextInput(Widget):
#     def __init__(self, initial=None, placeholder=None, readonly=False, **style):
#         default_style = {
#             'margin': 8
#         }
#         default_style.update(style)
#         super(TextInput, self).__init__(**default_style)
#         self.placeholder = placeholder
#
#         self.startup()
#
#         self.value = initial
#         # self.readonly = readonly
#
#     def startup(self):
#         self._impl = EditText(App._impl)
#         if self.placeholder:
#             self._impl.setHint(self.placeholder)
#
#     @property
#     def readonly(self):
#         return self._readonly
#
#     @readonly.setter
#     def readonly(self, value):
#         self._readonly = value
#         # self._impl.setEditable_(not self._readonly)
#
#     @property
#     def value(self):
#         return self._impl.getText().toString()
#
#     @value.setter
#     def value(self, value):
#         if value:
#             self._impl.setText(value)
