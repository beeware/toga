from rubicon.objc import NSSize

from toga_cocoa.libs import NSImage


class Icon:
    EXTENSIONS = [".icns", ".png", ".pdf"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.interface._impl = self
        self.path = path
        try:
            # We *should* be able to do a direct NSImage.alloc.init...(), but if the
            # image file is invalid, the init fails, and returns NULL - but we've
            # created an ObjC instance, so when the object passes out of scope, Rubicon
            # tries to free it, which segfaults. To avoid this, we retain result of the
            # alloc() (overriding the default Rubicon behavior of alloc), then release
            # that reference once we're done. If the image was created successfully, we
            # temporarily have a reference count that is 1 higher than it needs to be;
            # if it fails, we don't end up with a stray release.
            image = NSImage.alloc().retain()
            self.native = image.initWithContentsOfFile(str(path))
            if self.native is None:
                raise ValueError(f"Unable to load icon from {path}")
        finally:
            image.release()

        # Multiple icon interface instances can end up referencing the same native
        # instance, so make sure we retain a reference count at the impl level.
        self.native.retain()

    def __del__(self):
        if self.native:
            self.native.release()

    def _as_size(self, size):
        image = self.native.copy()
        image.setSize(NSSize(size, size))
        return image
