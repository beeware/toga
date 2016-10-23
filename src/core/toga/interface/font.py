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
        raise NotImplementedError(
            'Platform implementation must define create()')

    @property
    def family(self):
        return self._family

    @property
    def size(self):
        return self._size
