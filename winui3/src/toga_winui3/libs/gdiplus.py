from ctypes import POINTER, WinError, byref, cast
from ctypes.wintypes import UINT

import win32more.Windows.Win32.Graphics.GdiPlus as gdi_plus
from win32more import String
from win32more.Windows.Win32.Foundation import BOOL, UIntPtr
from win32more.Windows.Win32.Graphics.GdiPlus import (
    FontStyleBold,
    FontStyleBoldItalic,
    FontStyleItalic,
    FontStyleRegular,
    FontStyleStrikeout,
    FontStyleUnderline,
    GdiplusStartupInput,
    GdiplusStartupOutput,
    GpBitmap,
    GpFontFamily,
    GpImage,
)
from win32more.Windows.Win32.UI.WindowsAndMessaging import HICON

########################################################################################
# GDI+ return status processing.
########################################################################################

# https://learn.microsoft.com/en-us/windows/win32/gdiplus/-gdiplus-flatapi-flat
# https://learn.microsoft.com/windows/win32/api/Gdiplustypes/ne-gdiplustypes-status
STATUS_DICT = {
    0: "Ok",
    1: "GenericError",
    2: "InvalidParameter",
    3: "OutOfMemory",
    4: "ObjectBusy",
    5: "InsufficientBuffer",
    6: "NotImplemented",
    7: "Win32Error",
    8: "WrongState",
    9: "Aborted",
    10: "FileNotFound",
    11: "ValueOverflow",
    12: "AccessDenied",
    13: "UnknownImageFormat",
    14: "FontFamilyNotFound",
    15: "FontStyleNotFound",
    16: "NotTrueTypeFont",
    17: "UnsupportedGdiplusVersion",
    18: "GdiplusNotInitialized",
    19: "PropertyNotFound",
    20: "PropertyNotSupported",
    21: "ProfileNotFound",
}


def gdi_plus_function(function):
    def wrapper(*args, **kwargs):
        status_code = function(*args, **kwargs)
        if status_code != 0 and status_code is not None:
            error = str(STATUS_DICT[status_code])
            function_name = str(function._prototype.__name__)
            message = f"The GDI+ function {function_name} exit with status {error}."

            raise WinError(descr=message)

    return wrapper


########################################################################################
# GDI+ context manager.
########################################################################################

# Wrap functions to check exit status code.
GdiplusStartup = gdi_plus_function(gdi_plus.GdiplusStartup)
GdiplusShutdown = gdi_plus_function(gdi_plus.GdiplusShutdown)


class GdiPlusContext:
    """A context manager for running GdiPlus functions."""

    def __init__(self):
        self._input = GdiplusStartupInput()
        self._input.GdiplusVersion = 1
        self._input.DebugEventCallback = 0
        self._input.SuppressBackgroundThread = BOOL(0)
        self._input.SuppressExternalCodecs = BOOL(0)

        self._token = UIntPtr()
        self._output = GdiplusStartupOutput()

    def __enter__(self):
        GdiplusStartup(byref(self._token), byref(self._input), byref(self._output))

    def __exit__(self, exc_type, exc_value, traceback):
        GdiplusShutdown(self._token)


gdi_plus_context = GdiPlusContext()


########################################################################################
# GDI+ fonts
########################################################################################

ALL_FONT_STYLES = (
    FontStyleRegular
    | FontStyleBold
    | FontStyleItalic
    | FontStyleBoldItalic
    | FontStyleUnderline
    | FontStyleStrikeout
)


FontFamilyPtr = POINTER(GpFontFamily)


# Wrap functions to check exit status code.
GdipCreateFontFamilyFromName = gdi_plus_function(gdi_plus.GdipCreateFontFamilyFromName)
GdipIsStyleAvailable = gdi_plus_function(gdi_plus.GdipIsStyleAvailable)


def is_font_installed(font_family_name: str):
    """Checks whether a font is installed on the current system.

    Note that the font family name must be exactly as it appears in the Windows Settings
    under Personalization > Fonts.

    For example, "Times New Roman" will load but variations such as "Times New", "Times
    New Roman Bold" will not.
    """
    with gdi_plus_context:
        font_family_ptr = FontFamilyPtr()
        font_available = BOOL()

        try:
            # Attempt to create the font family.
            GdipCreateFontFamilyFromName(
                String(font_family_name),
                None,
                byref(font_family_ptr),
            )

            # Check if the font family has been created.
            GdipIsStyleAvailable(
                font_family_ptr, ALL_FONT_STYLES, byref(font_available)
            )

        except OSError:
            return False

    return font_available.value == 1


########################################################################################
# GDI+ icons
########################################################################################

BitmapPtr = POINTER(GpBitmap)
ImagePtr = POINTER(GpImage)


# Wrap functions to check exit status code.
GdipCreateBitmapFromFile = gdi_plus_function(gdi_plus.GdipCreateBitmapFromFile)
GdipCreateBitmapFromHICON = gdi_plus_function(gdi_plus.GdipCreateBitmapFromHICON)
GdipCreateHICONFromBitmap = gdi_plus_function(gdi_plus.GdipCreateHICONFromBitmap)
GdipBitmapGetPixel = gdi_plus_function(gdi_plus.GdipBitmapGetPixel)
GdipGetImageHeight = gdi_plus_function(gdi_plus.GdipGetImageHeight)
GdipGetImageWidth = gdi_plus_function(gdi_plus.GdipGetImageWidth)


def create_icon(icon_path: str) -> HICON:
    """Creates a Win32 icon from a file."""
    bitmap_ptr = BitmapPtr()
    icon_handle = HICON()

    with gdi_plus_context:
        GdipCreateBitmapFromFile(String(icon_path), byref(bitmap_ptr))
        GdipCreateHICONFromBitmap(bitmap_ptr, byref(icon_handle))

    return icon_handle


def color_to_rgba(color):
    return (
        (color >> 16) & 0b11111111,  # Red
        (color >> 8) & 0b11111111,  # Green
        color & 0b11111111,  # Blue
        (color >> 24) & 0b11111111,  # Alpha
    )


def icon_pixels(icon_handle: HICON):
    bitmap_ptr = BitmapPtr()
    pixel_array = []

    with gdi_plus_context:
        GdipCreateBitmapFromHICON(icon_handle, byref(bitmap_ptr))
        image_ptr = cast(bitmap_ptr, ImagePtr)

        width = UINT()
        height = UINT()
        GdipGetImageWidth(image_ptr, byref(width))
        GdipGetImageHeight(image_ptr, byref(height))

        color = UINT()
        for x in range(width.value):
            pixel_array.append([])
            for y in range(height.value):
                GdipBitmapGetPixel(bitmap_ptr, x, y, byref(color))
                argb = color_to_rgba(color.value)
                pixel_array[x].append(argb)

    return pixel_array
