from pathlib import Path

import __main__
import toga
from toga import App


class Paths:
    # Allow instantiating Path object via the factory
    Path = Path

    @property
    def app(self):
        return Path(__main__.__file__).parent

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
