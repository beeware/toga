from pathlib import Path

from rubicon.objc import NSSize

from toga_cocoa.libs import NSBundle, NSImage


class Icon:
    EXTENSIONS = [".icns", ".png", ".pdf"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.interface._impl = self

        if path is None:
            # Look to the app bundle, and get the icon. Set self.path as None
            # as an indicator that this is the app's default icon.
            # This bundle icon file definition might not contain an extension,
            # even thought the actual file will; so force the .icns extension.
            bundle_icon = NSBundle.mainBundle.objectForInfoDictionaryKey(
                "CFBundleIconFile"
            )
            if bundle_icon is None:
                # Not an .app bundle (e.g., POSIX build made with PyInstaller)
                # This can't be tested as the testbed app is bundled by Briefcase.
                raise FileNotFoundError()  # pragma: no cover
            path = NSBundle.mainBundle.pathForResource(
                Path(bundle_icon).stem,
                ofType=".icns",
            )
            # If the icon file doesn't exist, raise the problem as FileNotFoundError
            # This can't be tested, as the app will always have an icon.
            if not Path(path).is_file():
                raise FileNotFoundError()  # pragma: no cover

            self.path = None
        else:
            self.path = path

        try:
            # We *should* be able to do a direct NSImage.alloc.init...(), but if the
            # image file is invalid, the init fails, returns NULL, and releases the
            # Objective-C object. Since we've created an ObjC instance, when the
            # object passes out of scope, Rubicon tries to free it, which segfaults.
            # To avoid this, we retain result of the alloc() (overriding the default
            # Rubicon behavior of alloc), then release that reference once we're
            # done. If the image was created successfully, we temporarily have a
            # reference count that is 1 higher than it needs to be; if it fails, we
            # don't end up with a stray release.
            image = NSImage.alloc().retain()
            self.native = image.initWithContentsOfFile(str(path))
            if self.native is None:
                raise ValueError(f"Unable to load icon from {path}")
        finally:
            # Calling `release` here disabled Rubicon's "release on delete" automation.
            # We therefore add an explicit `release` call in __del__ if the NSImage was
            # initialized successfully.
            image.release()

    def __del__(self):
        if self.native:
            self.native.release()

    def _as_size(self, size):
        image = self.native.copy()
        image.setSize(NSSize(size, size))
        return image
