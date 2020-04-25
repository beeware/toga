import sys
from pathlib import Path

import toga
from toga import App


class Paths:
    # Allow instantiating Path object via the factory
    Path = Path

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

    @property
    def toga(self):
        """Return a path to a Toga system resources
        """
        return Path(toga.__file__).parent


paths = Paths()
