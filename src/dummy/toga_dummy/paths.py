import sys
from pathlib import Path

from toga import App


class Paths:
    @property
    def app(self):
        return Path(sys.modules[App.app.module_name].__file__).parent

    @property
    def data(self):
        return Path.home() / 'user_data' / App.app.app_id

    @property
    def cache(self):
        return Path.home() / 'cache' / App.app.app_id

    @property
    def logs(self):
        return Path.home() / 'logs' / App.app.app_id

    def sys_resource(self, next_to):
        """Return a path to a Toga system resource that resides next to the
        given Python source file

        Args:
            next_to (str): A Python source file the resource is next to
        """
        return Path(next_to).parent

    def arbitrary(self, path):
        """Return an arbitrary path representing object

        Args:
            path (str): A string with the path to wrap. If a relative path is
                        given, it will be interpreted to be relative to the
                        application module directory.
        """
        return self.app / Path(path)


paths = Paths()
