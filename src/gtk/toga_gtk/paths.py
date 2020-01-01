import sys
from pathlib import Path

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


paths = Paths()
