# from ..app import App
# from .base import WidgetMixin
#
#
# class ImageView(ImageViewInterface, WidgetMixin):
#     def __init__(self, image, **style):
#         default_style = {
#             'margin': 8
#         }
#         default_style.update(style)
#         super(ImageView, self).__init__(**default_style)
#
#         self.startup()
#
#         self.value = initial
#         # self.readonly = readonly
#
#     def startup(self):
#         self._impl = ImageView(App._impl)
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
