import os


class ClassProperty(property):
    """ This class makes it possible to use a classmethod like a property.

    Warnings:
        Only works for getting not for setting.
    """

    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class Icon:
    """ Icon widget.

    Icon is a deferred resource; it's impl isn't available until it is
    requested; the factory is provided at the time the implementation is
    requested.

    Args:
        path(str): Path to the icon file.
        system(bool): Set to `True if the icon is located in the 'resource' folder
            of the Toga package. Default is False.
    """

    def __init__(self, path, system=False):
        self.filename = None

        if os.path.splitext(path)[1] in ('.png', '.icns', '.bmp'):
            self.path = path
        else:
            self.path = path + '.icns'

        self.system = system
        if self.system:
            toga_dir = os.path.dirname(os.path.dirname(__file__))
            self.filename = os.path.join(toga_dir, 'resources', self.path)
        else:
            from toga.app import App
            self.filename = os.path.join(App.app_dir, self.path)

        self.__impl = None

    def _impl(self, factory=None):
        if self.__impl is None:
            self.__impl = factory.Icon(interface=self)
        return self.__impl

    @classmethod
    def load(cls, path_or_icon, default=None):
        if path_or_icon:
            if isinstance(path_or_icon, Icon):
                obj = path_or_icon
            else:
                obj = cls(path_or_icon)
        elif default:
            obj = default

        return obj

    @ClassProperty
    @classmethod
    def TIBERIUS_ICON(cls):
        """ Tiberius it the mascot of the Toga Project and is therefore
        shipped with Toga.

        Returns:
            Returns the Tiberius icon `toga.Icon`.
       """
        return cls('tiberius', system=True)
