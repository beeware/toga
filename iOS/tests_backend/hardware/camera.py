import sqlite3
import sys
from pathlib import Path

import pytest

import toga
from toga_iOS.hardware.camera import Camera
from toga_iOS.libs import (
    NSBundle,
    UIImagePickerController,
    UIImagePickerControllerCameraDevice,
)

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

        # iPhone simulator has no camera devices. Mock the response of the camera
        # identifiers to report a rear camera with a flash, and a front camera with
        # no flash.

        def _is_available(self, device):
            return True

        def _has_flash(self, device):
            return device == UIImagePickerControllerCameraDevice.Rear

        monkeypatch.setitem(
            UIImagePickerController.objc_class.__dict__["instance_methods"],
            "isCameraDeviceAvailable:",
            _is_available,
        )
        monkeypatch.setitem(
            UIImagePickerController.objc_class.__dict__["instance_methods"],
            "isFlashAvailableForCameraDevice:",
            _has_flash,
        )

    def cleanup(self):
        picker = self.app.camera._impl.native
        try:
            result = picker.result
            if not result.future.done():
                picker.imagePickerControllerDidCancel(picker)
        except AttributeError:
            pass

    def known_cameras(self):
        return {
            "Rear": ("Rear", True),
            "Front": ("Front", False),
        }

    def select_other_camera(self):
        raise pytest.xfail("Cannot programmatically change camera on iOS")

    def disconnect_cameras(self):
        raise pytest.xfail("Cameras cannot be removed on iOS")

    def reset_permission(self):
        # Mock the *next* call to retrieve photo permission.
        orig = Camera.has_permission

        def reset_permission(mock, allow_unknown=False):
            self.monkeypatch.setattr(Camera, "has_permission", orig)
            return allow_unknown

        self.monkeypatch.setattr(Camera, "has_permission", reset_permission)

    def allow_permission(self):
        # Mock the result of has_permission to allow
        def grant_permission(mock, allow_unknown=False):
            return True

        self.monkeypatch.setattr(Camera, "has_permission", grant_permission)

    def reject_permission(self):
        # Mock the result of has_permission to deny
        def deny_permission(mock, allow_unknown=False):
            return False

        self.monkeypatch.setattr(Camera, "has_permission", deny_permission)

    async def wait_for_camera(self):
        await self.redraw("Camera view displayed", delay=0.5)

    async def press_shutter_button(self, photo):
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

        return await photo, None, None

    async def cancel_photo(self, photo):
        # Fake the result of a cancelling the photo
        picker = self.app.camera._impl.native
        picker.imagePickerControllerDidCancel(picker)

        await self.redraw("Photo cancelled", delay=0.5)

        return await photo

    def same_device(self, device, native):
        # As the iOS camera is an external UI, we can't programmatically influence or
        # modify it; so we make all device checks pass.
        return True

    def same_flash_mode(self, expected, actual):
        # As the iOS camera is an external UI, we can't programmatically influence or
        # modify it; so we make all device checks pass.
        return True
