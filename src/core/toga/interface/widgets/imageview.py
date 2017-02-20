from .base import Widget


class ImageView(Widget):
    '''
    An image viewer
    '''
    def __init__(self, id=None, style=None, image=None):
        '''
        Instantiate a new image viewer widget
        
        :param id:          An identifier for this widget.
        :type  id:          ``str``
    
        :param style:       an optional style object. If no style is provided then a
                            new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`
    
        :param image:    Image to display
        '''
        super().__init__(id=id, style=style, image=image)

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
