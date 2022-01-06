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
        return Path(App.app._impl.native.getApplicationContext().getFilesDir().getPath())

    @property
    def cache(self):
        return Path(App.app._impl.native.getApplicationContext().getCacheDir().getPath())

    @property
    def logs(self):
        return Path(App.app._impl.native.getApplicationContext().getCacheDir().getPath()) / 'log'

    @property
    def toga(self):
        """Return a path to a Toga resources
        """
        return Path(toga.__file__).parent


paths = Paths()
