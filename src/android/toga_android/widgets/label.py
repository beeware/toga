# from ..app import MobileApp
# from .base import Widget
#
# from toga.constants import *
#
#
# class Label(Widget):
#     def __init__(self, text=None, alignment=LEFT_ALIGNED):
#         super(Label, self).__init__()
#
#         self.startup()
#
#         self.alignment = alignment
#         self.text = text
#
#     def startup(self):
#         print ("startup label")
#         self._impl = TextView(MobileApp._impl)
#
#     @property
#     def alignment(self):
#         return self._alignment
#
#     @alignment.setter
#     def alignment(self, value):
#         self._alignment = value
#         self._impl.setGravity({
#                 LEFT_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.LEFT,
#                 RIGHT_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.RIGHT,
#                 CENTER_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
#                 JUSTIFIED_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
#                 NATURAL_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
#             }[value])
#
#     @property
#     def text(self):
#         return self._text
#
#     @text.setter
#     def text(self, value):
#         self._text = value
#         self._impl.setHint(self._text)
