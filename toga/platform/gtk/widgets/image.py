import os


class Image(object):
    app_icon = None

    def __init__(self, path, system=False):
        self.path = path
        self.system = system

        if self.system:
            filename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'resources', self.path)
        else:
            filename = self.path

        # self._impl = NSImage.alloc().initWithContentsOfFile_(get_NSString(filename))

    @staticmethod
    def load(path_or_icon, default=None):
        if path_or_icon:
            if isinstance(path_or_icon, Image):
                impl = path_or_icon
            else:
                impl = Image(path_or_icon)
        elif default:
            impl = default
        return impl


TIBERIUS_ICON = Image('tiberius.icns', system=True)
