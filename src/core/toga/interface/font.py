class Font:
    """
    A `Font` is a font family (e.g. "Helvetica") and a size (e.g. 15) that can
    be applied to widgets.
    """
    def __init__(self, family, size):
        self._family = family
        self._size = size
        self.create()

    def create(self):
        '''
        Create font
        '''
        raise NotImplementedError(
            'Platform implementation must define create()')

    @property
    def family(self):
        '''
        Font family, e.g. Helvetica
        
        :rtype: ``str``
        '''
        return self._family

    @property
    def size(self):
        '''
        Font size
        
        :rtype: ``int``
        '''
        return self._size
