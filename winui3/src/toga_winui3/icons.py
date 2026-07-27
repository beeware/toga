from pathlib import Path

from win32more.Microsoft.UI import IconId
from win32more.Microsoft.UI.Interop import GetIconIdFromIcon
from win32more.Microsoft.UI.Xaml.Controls import ImageIcon
from win32more.Microsoft.UI.Xaml.Media.Imaging import BitmapImage
from win32more.Windows.Foundation import Uri
from win32more.Windows.Win32.Foundation import PWSTR
from win32more.Windows.Win32.UI.WindowsAndMessaging import (
    HICON,
    IMAGE_ICON,
    LR_LOADFROMFILE,
    LoadImageW,
)

from .libs.gdiplus import create_icon
from .libs.nativeevents import events_handled


def load_icon(path: str) -> HICON:
    """Creates an icon resource from an .ico file."""
    hwnd = LoadImageW(None, PWSTR(path), IMAGE_ICON, 0, 0, LR_LOADFROMFILE)
    if hwnd is None:
        raise OSError(f"LoadImageW failed to load {path}.")
    return HICON(hwnd)


class Icon:
    """The Icon implementation for the WinUI 3 backend.

    The WinUI 3 backend needs two type of icon:
        - Native WinUI 3 - to be used with most native WinUI 3 classes such as button.
        - Win32 - to be used with StatusIcons the title bar.

    To avoid loading unnecessary resources, the needed icon resources are lazy loaded.
    """

    EXTENSIONS = [".png", ".ico", ".bmp", ".jpg", ".jpeg", ".gif", ".tif", ".tiff"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self._handle: None | HICON = None
        self._id: None | IconId = None
        self._bitmap_image: None | BitmapImage = None

        if path is None:
            raise ValueError(
                f"Unable to use path={path}. The app bundle icon is not implemented."
            )
        else:
            self.path = Path(path)

    @property
    def uri(self) -> Uri:
        return Uri(f"file:///{self.path.as_posix()}")

    def _use_default_icon(self, property):
        print(
            f"WARNING: Unable to load icon {self.path}; falling back to default icon."
        )
        self.path = Path(__file__).parent / "resources" / "toga.png"
        return getattr(self, property)

    @property
    def handle(self) -> HICON:
        """The handle to the Win32 icon object created using the icon's path."""
        if self._handle is None:
            try:
                if self.path.suffix != ".ico":
                    self._handle = create_icon(str(self.path))
                else:
                    self._handle = load_icon(str(self.path))
            except OSError:
                return self._use_default_icon("handle")

        return self._handle

    @property
    def id(self) -> IconId:
        """The IconId to the WinRT icon object created using the icon's path."""
        if self._id is None:
            self._id = GetIconIdFromIcon(self.handle)

        return self._id

    @property
    def bitmap_image(self) -> BitmapImage:
        """The WinUI 3 BitmapImage used as a source for the icon."""
        if self._bitmap_image is None:
            self._bitmap_image = events_handled(BitmapImage)
            self._bitmap_image.event_handler.ImageFailed += (
                self.native_event_image_failed
            )
            self._bitmap_image.UriSource = self.uri

        return self._bitmap_image

    def native_event_image_failed(self, sender, args):
        self._bitmap_image.UriSource = self._use_default_icon("uri")

    def image_icon(self, size=16):
        """The WinUI 3 icon implementation."""
        image_icon = ImageIcon()
        image_icon.Height = size
        image_icon.Width = size
        image_icon.Source = self.bitmap_image

        return image_icon
