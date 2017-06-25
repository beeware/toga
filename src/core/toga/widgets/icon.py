import os
from ..platform import get_platform_factory


class Icon:
    app_icon = None

    def __init__(self, path, system=False, factory=None):
        if os.path.splitext(path)[1] in ('.png', '.icns', '.bmp'):
            self.path = path
        else:
            self.path = path + self.EXTENSION
        self.system = system

        if self.system:
            toga_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

            self.filename = os.path.join(toga_dir, 'resources', self.path)
        else:
            self.filename = self.path

        if factory is None:
            self.factory = get_platform_factory()
        else:
            self.factory = factory
        self._impl = self.factory.Icon(creator=self)
        self._create()
        self._configure()

        # self.create(filename)

    def _create(self):
        self._impl.create(self.filename)

    def _configure(self):
        pass

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
