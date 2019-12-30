import sys
from pathlib import Path

from toga import App


class Paths:
    @property
    def app(self):
        return Path(sys.modules[App.app.app_module].__file__).parent

    @property
    def data(self):
        return Path.home() / 'AppData' / 'Local' / App.app.author / App.app.name

    @property
    def cache(self):
        return Path.home() / 'Library' / 'Local' / App.app.author / App.app.name / 'Cache'

    @property
    def logs(self):
        return Path.home() / 'Library' / 'Local' / App.app.author / App.app.name / 'Logs'
