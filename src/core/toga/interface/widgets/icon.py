import os


class Icon:
    app_icon = None

    def __init__(self, path, system=False):
        self.path = path
        self.system = system

        if self.system:
            toga_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            filename = os.path.join(toga_dir, 'resources', self.path + self.EXTENSION)
        else:
            filename = self.path + self.EXTENSION

        self.create(filename)

    def create(self, filename):
        raise NotImplementedError('Icon must define create()')

    @staticmethod
    def load(path_or_icon, default=None):
        if path_or_icon:
            if isinstance(path_or_icon, Icon):
                obj = path_or_icon
            else:
                obj = Icon(path_or_icon)
        elif default:
            obj = default
        return obj
