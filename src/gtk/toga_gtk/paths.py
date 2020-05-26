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
    def data(self):
        return Path.home() / '.local' / 'share' / App.app.name

    @property
    def cache(self):
        return Path.home() / '.cache' / App.app.name

    @property
    def logs(self):
        return Path.home() / '.cache' / App.app.name / 'log'

    @property
    def toga(self):
        """Return a path to a Toga resources
        """
        return Path(toga.__file__).parent


paths = Paths()
