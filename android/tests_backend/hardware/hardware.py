from unittest.mock import Mock

from android.content.pm import PackageManager

from toga_android.app import App

from ..app import AppProbe


class HardwareProbe(AppProbe):

    def __init__(self, monkeypatch, app_probe):
        super().__init__(app_probe.app)

        self.monkeypatch = monkeypatch

        # A mocked permissions table. The key is the media type; the value is True
        # if permission has been granted, False if it has be denied. A missing value
        # will be turned into a grant if permission is requested.
        self._mock_permissions = {}

        # Mock App.startActivityForResult
        self._mock_startActivityForResult = Mock()
        monkeypatch.setattr(
            App, "_native_startActivityForResult", self._mock_startActivityForResult
        )

        # Mock App.requestPermissions
        def request_permissions(permissions, code):
            grants = []
            for permission in permissions:
                status = self._mock_permissions.get(permission, 0)
                self._mock_permissions[permission] = abs(status)
                grants.append(
                    PackageManager.PERMISSION_GRANTED
                    if status
                    else PackageManager.PERMISSION_DENIED
                )

            app_probe.app._impl._listener.onRequestPermissionsResult(
                code, permissions, grants
            )

        self._mock_requestPermissions = Mock(side_effect=request_permissions)
        monkeypatch.setattr(
            App, "_native_requestPermissions", self._mock_requestPermissions
        )

        # Mock ContextCompat.checkSelfPermission
        def has_permission(permission):
            return (
                PackageManager.PERMISSION_GRANTED
                if self._mock_permissions.get(permission, 0) == 1
                else PackageManager.PERMISSION_DENIED
            )

        self._mock_checkSelfPermission = Mock(side_effect=has_permission)
        monkeypatch.setattr(
            app_probe.app._impl,
            "_native_checkSelfPermission",
            self._mock_checkSelfPermission,
        )

    def cleanup(self):
        pass
