import sys
from pathlib import Path

from toga import App


class Paths:
    @property
    def app(self):
        return Path(sys.modules[App.app.module_name].__file__).parent

    @property
    def author(self):
        if App.app.author is None:
            return "Unknown Developer"
        return App.app.author

    @property
    def data(self):
        return Path.home() / 'AppData' / 'Local' / self.author / App.app.formal_name

    @property
    def cache(self):
        return Path.home() / 'Library' / 'Local' / self.author / App.app.formal_name / 'Cache'

    @property
    def logs(self):
        return Path.home() / 'Library' / 'Local' / self.author / App.app.formal_name / 'Logs'

    def sys_resource(self, next_to):
        """Return a path to a Toga system resource that resides next to the
        given Python source file

        Args:
            next_to (str): A Python source file the resource is next to
        """
        return Path(next_to).parent


paths = Paths()
