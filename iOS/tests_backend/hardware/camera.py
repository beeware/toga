import sqlite3
import sys
from pathlib import Path

import pytest

import toga
from toga_iOS.hardware.camera import Camera
from toga_iOS.libs import NSBundle

from ..app import AppProbe


class CameraProbe(AppProbe):
    def __init__(self, monkeypatch, app_probe):
        if not sys.implementation._simulator:
            pytest.skip("Can't run Camera tests on physical hardware")

        super().__init__(app_probe.app)

        self.monkeypatch = monkeypatch

        # iOS doesn't allow for permissions to be changed once they're initially set.
        # Since we need permissions to be enabled to test most features, set the
        # state of the TCC database to enable camera permissions when they're actually
        # interrogated by the UIKit APIs.
        tcc_db = sqlite3.connect(
            str(
                Path(NSBundle.mainBundle.resourcePath)
                / "../../../../../Library/TCC/TCC.db"
            ),
        )
        cursor = tcc_db.cursor()
        cursor.execute(
            (
                "REPLACE INTO access "
                "(service, client, client_type, auth_value, auth_reason, auth_version, flags) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)"
            ),
            ("kTCCServiceCamera", "org.beeware.toga.testbed", 0, 2, 2, 1, 0),
        )
        tcc_db.commit()
        tcc_db.close()

    def known_cameras(self):
        # iPhone simulator has no camera devices
        return []

    def has_flash(self, camera):
        return False

    def reset_photo_permission(self):
        # Mock the *next* call to retrieve photo permission.
        orig = Camera.has_photo_permission

        def reset_permission(mock, allow_unknown=False):
            self.monkeypatch.setattr(Camera, "has_photo_permission", orig)
            return allow_unknown

        self.monkeypatch.setattr(Camera, "has_photo_permission", reset_permission)

    def grant_photo_permission(self):
        # Mock the result of has_photo_permission to allow
        def grant_permission(mock, allow_unknown=False):
            return True

        self.monkeypatch.setattr(Camera, "has_photo_permission", grant_permission)

    def deny_photo_permission(self):
        # Mock the result of has_photo_permission to deny
        def deny_permission(mock, allow_unknown=False):
            return False

        self.monkeypatch.setattr(Camera, "has_photo_permission", deny_permission)

    async def take_photo(self, photo):
        await self.redraw("Camera view displayed", delay=0.5)

        # Fake the result of a successful photo being taken
        image = toga.Image("resources/photo.png")
        picker = self.app.camera._impl.native
        picker.imagePickerController(
            picker,
            didFinishPickingMediaWithInfo={
                "UIImagePickerControllerOriginalImage": image._impl.native
            },
        )

        await self.redraw("Photo taken", delay=0.5)

        return await photo

    async def cancel_photo(self, photo):
        await self.redraw("Camera view displayed", delay=0.5)

        # Fake the result of a cancelling the photo
        picker = self.app.camera._impl.native
        picker.imagePickerControllerDidCancel(picker)

        await self.redraw("Photo cancelled", delay=0.5)

        return await photo
