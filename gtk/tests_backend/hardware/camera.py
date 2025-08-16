from ..app import AppProbe


class CameraProbe(AppProbe):
    # Linux cannot support this because permission must be
    # requested before devices can be listed, and it's only possible
    # to reach the "first use" if a device is already identified
    request_permission_on_first_use = False

    def __init__(self, monkeypatch, app_probe):
        self._verify_dependencies()
        super().__init__(app_probe.app)

    def cleanup(self): ...

    def _verify_dependencies(self): ...

    def allow_permission(self): ...
