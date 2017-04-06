import os


class Icon:
    app_icon = None

    def __init__(self, path, system=False):
        if os.path.splitext(path)[1] in ('.png', '.icns', '.bmp'):
            self.path = path
        else:
            self.path = path + self.EXTENSION
        self.system = system


        if self.system:
            toga_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

            filename = os.path.join(toga_dir, 'resources', self.path)
        else:
            filename = self.path

        self.create(filename)

    def create(self, filename):
        raise NotImplementedError('Icon must define create()')

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
