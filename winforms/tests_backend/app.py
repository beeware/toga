from pathlib import Path

import System.Windows.Forms as WinForms

from .probe import BaseProbe


class AppProbe(BaseProbe):
    def __init__(self, app):
        super().__init__()
        self.app = app
        # The Winforms Application class is a singleton instance
        assert self.app._impl.native == WinForms.Application

    @property
    def config_path(self):
        return (
            Path.home()
            / "AppData"
            / "Local"
            / "Tiberius Yak"
            / "Toga Testbed"
            / "Config"
        )

    @property
    def data_path(self):
        return (
            Path.home() / "AppData" / "Local" / "Tiberius Yak" / "Toga Testbed" / "Data"
        )

    @property
    def cache_path(self):
        return (
            Path.home()
            / "AppData"
            / "Local"
            / "Tiberius Yak"
            / "Toga Testbed"
            / "Cache"
        )

    @property
    def logs_path(self):
        return (
            Path.home() / "AppData" / "Local" / "Tiberius Yak" / "Toga Testbed" / "Logs"
        )
