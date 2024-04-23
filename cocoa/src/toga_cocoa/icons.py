from rubicon.objc import NSSize

from toga_cocoa.libs import NSApplication, NSImage


class Icon:
    EXTENSIONS = [".icns", ".png", ".pdf"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.interface._impl = self
        self._needs_release = False

        self.path = path
        if path is None:
            # Can't use toga.App here, as the app impl may not have been created.
            self.native = NSApplication.sharedApplication.applicationIconImage
        else:
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
                else:
                    self._needs_release = True
            finally:
                # Calling `release` here disabled Rubicon's "release on delete" automation.
                # We therefore add an explicit `release` call in __del__ if the NSImage was
                # initialized successfully.
                image.release()

    def __del__(self):
        if self._needs_release:
            self.native.release()

    def _as_size(self, size):
        image = self.native.copy()
        image.setSize(NSSize(size, size))
        return image
