import sys
from pathlib import Path

import toga
from toga import App


class Paths:
    @property
    def app(self):
        return Path(sys.modules[App.app.module_name].__file__).parent

    @property
    def data(self):
        return Path.home() / '.local' / 'share' / App.app.name

    @property
    def cache(self):
        return Path.home() / '.cache' / App.app.name

    @property
    def logs(self):
        return Path.home() / '.cache' / App.app.name / 'log'

    @property
    def sys_resources(self):
        """Return a path to a Toga system resources
        """
        return Path(toga.__file__).parent

    def arbitrary(self, path):
        """Return an arbitrary path representing object

        Args:
            path (str): A string with the path to wrap. If a relative path is
                        given, it will be interpreted to be relative to the
                        application module directory.
        """
        return self.app / Path(path)


paths = Paths()
