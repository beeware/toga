from android.graphics import Bitmap, BitmapFactory, Rect
from android.graphics.drawable import BitmapDrawable


class Icon:
    EXTENSIONS = [".png"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.interface._impl = self

        if path is None:
            raise FileNotFoundError("No runtime app icon")

        self.path = path

        self.native = BitmapFactory.decodeFile(str(path))
        if self.native is None:
            raise ValueError(f"Unable to load icon from {path}")

    def as_drawable(self, widget, size):
        bitmap = Bitmap.createScaledBitmap(
            self.native,
            widget.scale_in(size),
            widget.scale_in(size),
            True,
        )
        drawable = BitmapDrawable(widget.native.getContext().getResources(), bitmap)
        drawable.setBounds(
            Rect(0, 0, drawable.getIntrinsicWidth(), drawable.getIntrinsicHeight())
        )
        return drawable
