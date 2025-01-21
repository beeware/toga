import sys
from pathlib import Path

import toga
from toga.platform import get_platform_factory


class Paths:
    def __init__(self):
        self.factory = get_platform_factory()
        self._impl = self.factory.Paths(self)

    @property
    def toga(self) -> Path:
        """The path that contains the core Toga resources.

        This path should be considered read-only. You should not attempt to write
        files into this path.
        """
        return Path(toga.__file__).parent

    @property
    def app(self) -> Path:
        """The path of the folder that contains the definition of the app class.

        This path should be considered read-only. You should not attempt to write
        files into this path.
        """
        app_module = sys.modules[toga.App.app.__module__]
        try:
            app_file = app_module.__file__
        except AttributeError:
            # At an interactive prompt, return the current working directory.
            return Path.cwd()
        else:
            return Path(app_file).parent

    @property
    def config(self) -> Path:
        """The platform-appropriate location for storing user configuration
        files associated with this app.
        """
        return self._impl.get_config_path()

    @property
    def data(self) -> Path:
        """The platform-appropriate location for storing user data associated
        with this app.
        """
        return self._impl.get_data_path()

    @property
    def cache(self) -> Path:
        """The platform-appropriate location for storing cache files associated
        with this app.

        It should be assumed that the operating system will purge the contents
        of this directory without warning if it needs to recover disk space.
        """
        return self._impl.get_cache_path()

    @property
    def logs(self) -> Path:
        """The platform-appropriate location for storing log files associated
        with this app.
        """
        return self._impl.get_logs_path()
