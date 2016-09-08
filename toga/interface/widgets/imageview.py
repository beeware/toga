from .base import Widget


class ImageView(Widget):
    def __init__(self, id=None, style=None, image=None):
        super().__init__(id=None, style=None, image=None)

    def _configure(self, image):
        self.image = image

    # @property
    # def alignment(self):
    #     return self._alignment

    # @alignment.setter
    # def alignment(self, value):
    #     self._alignment = value
    #     self._impl.setAlignment_(NSTextAlignment(self._alignment))

    # @property
    # def scaling(self):
    #     return self._scaling

    # @scaling.setter
    # def scaling(self, value):
    #     self._scaling = value
    #     self._impl.setAlignment_(NSTextAlignment(self._scaling))
