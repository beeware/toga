from ..app import AppProbe


class HardwareProbe(AppProbe):

    def __init__(self, monkeypatch, app_probe):
        super().__init__(app_probe.app)

        self.monkeypatch = monkeypatch
