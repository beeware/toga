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


paths = Paths()
