import sys
from pathlib import Path

import toga
from toga import App


class Paths:
    # Allow instantiating Path object via the factory
    Path = Path

    @property
    def __context(self):
        return App.app._impl.native.getApplicationContext()

    @property
    def app(self):
        return Path(sys.modules[App.app.module_name].__file__).parent

    @property
    def data(self):
        return Path(self.__context.getFilesDir().getPath())

    @property
    def cache(self):
        return Path(self.__context.getCacheDir().getPath())

    @property
    def logs(self):
        return self.data

    @property
    def toga(self):
        """Return a path to a Toga resources
        """
        return Path(toga.__file__).parent


paths = Paths()
