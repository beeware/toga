import ctypes
import io
from pathlib import Path

import System.Windows.Forms as WinForms
from PIL import Image, ImageSequence
from System.Drawing import Image as NetImage
from System.IO import MemoryStream

from .base import Widget


def _get_size(logical_size=32):
    """
    Get the size of the spinner to render to, as one integer representing
    both height and width.

    :param logical_size: The original size of the spinner.
    :type logical_size: int

    :return: The size for the spinner to resize to.
    :rtype: int
    """
    user32 = ctypes.windll.user32
    try:
        user32.SetProcessDPIAware()
        dpi = user32.GetDpiForSystem()
    except AttributeError:  # pragma: no cover
        dpi = 96
    physical_size = logical_size * dpi / 96
    return int(physical_size * 2.5)  # *2.5 to make it sharp on monitor


def _composite_gif_on_color(path: str, rgb_color: tuple, size: int) -> bytes:
    """
    Composite the spinner GIF onto a solid color background and resize it
    using bilinear interpolation.

    :param path: Path to the spinner GIF file
    :type path: str
    :param rgb_color: A tuple of three integers of the solid background color,
        in RGB format.
    :type rgb_color: tuple
    :param size: An integer representing the target size, both height and width since
        it is always a square.
    :type size: tuple

    :return: The processed GIF as a byte stream
    :rtype: bytes
    """
    with Image.open(path) as original_gif:
        composited_frames = []
        durations = []

        for frame in ImageSequence.Iterator(original_gif):
            frame = frame.convert("RGBA")
            background = Image.new("RGBA", frame.size, rgb_color + (255,))
            composited = Image.alpha_composite(background, frame)
            composited = composited.resize((size, size), Image.BILINEAR)
            composited_p = composited.convert("P", palette=Image.ADAPTIVE)
            composited_frames.append(composited_p)
            durations.append(frame.info.get("duration", 20))

        output_buffer = io.BytesIO()
        composited_frames[0].save(
            output_buffer,
            format="GIF",
            save_all=True,
            append_images=composited_frames[1:],
            loop=original_gif.info.get("loop", 0),
            duration=durations,
            disposal=2,
        )
        output_buffer.seek(0)
        return output_buffer.getvalue()


cache = dict()


def antialias_spinner(color: tuple):
    """
    Get the spinner image of a desired color as a byte stream.

    :type rgb_color: tuple
    :param size: The color background that the spinner is going to be on
    :type size: tuple

    :return: The processed GIF as a byte stream
    :rtype: bytes
    """
    size = _get_size()
    if color not in cache:
        cache[color] = NetImage.FromStream(
            MemoryStream(
                _composite_gif_on_color(
                    str(Path(__file__).parent.parent / "resources" / "spinner.gif"),
                    color,
                    size,
                )
            )
        )
    return cache[color]


class ActivityIndicator(Widget):
    def create(self):
        self.native = WinForms.PictureBox()
        self.native.Image = antialias_spinner(
            (self.native.BackColor.R, self.native.BackColor.G, self.native.BackColor.B)
        )
        self.native.SizeMode = WinForms.PictureBoxSizeMode.Zoom
        self.interface.intrinsic.width = 32
        self.interface.intrinsic.height = 32
        self.running = False

    def set_background_color(self, color):
        super().set_background_color(color)
        self.native.Image = antialias_spinner(
            (self.native.BackColor.R, self.native.BackColor.G, self.native.BackColor.B)
        )

    def set_hidden(self, hidden):
        self.native.Visible = self.running and not hidden
        self.hidden = hidden

    def is_running(self):
        return self.running

    def start(self):
        self.running = True
        self.native.Visible = not self.hidden

    def stop(self):
        self.native.Visible = False
        self.running = False

    def rehint(self):
        self.interface.intrinsic.width = 32
        self.interface.intrinsic.height = 32
