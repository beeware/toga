import sys
from pathlib import Path

import toga
from toga import App


class Paths:
    # Allow instantiating Path object via the factory
    Path = Path

    @property
    def app(self):
        try:
            return Path(sys.modules["__main__"].__file__).parent
        except KeyError:
            # If we're running in test conditions,
            # there is no __main__ module.
            return Path.cwd()
        except AttributeError:
            # If we're running at an interactive prompt,
            # the __main__ module isn't file-based.
            return Path.cwd()

    @property
    def author(self):
        if App.app.author is None:
            return "Toga"
        return App.app.author

    @property
    def data(self):
        return Path.home() / 'AppData' / 'Local' / self.author / App.app.formal_name

    @property
    def cache(self):
        return Path.home() / 'AppData' / 'Local' / self.author / App.app.formal_name / 'Cache'

    @property
    def logs(self):
        return Path.home() / 'AppData' / 'Local' / self.author / App.app.formal_name / 'Logs'

    @property
    def toga(self):
        """Return a path to a Toga system resources
        """
        return Path(toga.__file__).parent


paths = Paths()
