from toga.platform import get_platform_factory


class Font:
    def __init__(self, family, size, factory=None):
        """ A :obj:`Font` is a font family (e.g. "Helvetica") and a size (e.g. 15) that can
        be applied to widgets.

        Args:
            family (str): Name of the font family.
            size (int): Defines the display size of the font.
        """
        self._family = family
        self._size = size

        self.factory = get_platform_factory(factory)
        self._impl = self.factory.Font(interface=self)

    @property
    def family(self):
        """ Font family, e.g. Helvetica

        Returns:
            Returns a ``str`` with the name of the font family
        """
        return self._family

    @property
    def size(self):
        """ Font size

        Returns:
            The size of the font in ``int``.
        """
        return self._size
