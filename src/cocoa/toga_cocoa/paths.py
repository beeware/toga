import sys
from pathlib import Path

from toga import App


class Paths:
    @property
    def app(self):
        return Path(sys.modules[App.app.module_name].__file__).parent

    @property
    def data(self):
        return Path.home() / 'Library' / 'Application Support' / App.app.app_id

    @property
    def cache(self):
        return Path.home() / 'Library' / 'Caches' / App.app.app_id

    @property
    def logs(self):
        return Path.home() / 'Library' / 'Logs' / App.app.app_id


paths = Paths()
