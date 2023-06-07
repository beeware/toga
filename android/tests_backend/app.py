from pathlib import Path

from toga_android.libs.activity import MainActivity

from .probe import BaseProbe


class AppProbe(BaseProbe):
    def __init__(self, app):
        super().__init__()
        self.app = app
        assert isinstance(self.app._impl.native, MainActivity)

    def get_app_context(self):
        return self.app._impl.native.getApplicationContext()

    @property
    def config_path(self):
        return Path(self.get_app_context().getFilesDir().getPath()) / "config"

    @property
    def data_path(self):
        return Path(self.get_app_context().getFilesDir().getPath()) / "data"

    @property
    def cache_path(self):
        return Path(self.get_app_context().getCacheDir().getPath())

    @property
    def logs_path(self):
        return Path(self.get_app_context().getFilesDir().getPath()) / "log"
