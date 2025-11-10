from __future__ import annotations

import io
from pathlib import Path

import System.Windows.Forms as WinForms
from PIL import Image, ImageSequence
from System.Drawing import Image as WinImage
from System.IO import MemoryStream

from toga.colors import TRANSPARENT

from .base import Widget


def composite_gif_on_color(
    path: str, background_color: tuple[int, int, int], size: int
) -> bytes:
    """Composite the transparent spinner source GIF onto a solid color
    background, and resize it using bilinear interpolation.

    :param path: Path to the spinner GIF file
    :param background_color: The background color as an RGB integer triple.
    :param size: The target size of the image to generate.
    :return: The processed non-transparent animated GIF as a byte stream
    """
    with Image.open(path) as original_gif:
        composited_frames = []
        durations = []

        for frame in ImageSequence.Iterator(original_gif):
            frame = frame.convert("RGBA")
            background = Image.new("RGBA", frame.size, background_color + (255,))
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


class ActivityIndicator(Widget):
    SPINNER_SIZE = 32
    SPINNER_CACHE: dict[tuple[tuple[int, int, int], int], WinImage] = {}

    def create(self):
        self.native = WinForms.PictureBox()
        self.native.SizeMode = WinForms.PictureBoxSizeMode.Zoom
        self._spinner_cache_key = None
        self._default_background_color = TRANSPARENT
        self.set_spinner_image()
        self.running = False

    def set_spinner_image(self):
        """Set the spinner image, compositing against the current background
        color, and scaling to reflect the current display DPI.
        """
        background_color = (
            self.native.BackColor.R,
            self.native.BackColor.G,
            self.native.BackColor.B,
        )
        # Scale by 2.5 times over the pixel size to ensure a sharp image.
        size = int(self.scale_in(self.SPINNER_SIZE) * 2.5)
        cache_key = (background_color, size)

        # We only need to change the image if the cache key has changed.
        if self._spinner_cache_key != cache_key:
            self._spinner_cache_key = cache_key
            try:
                spinner_image = self.SPINNER_CACHE[cache_key]
            except KeyError:
                # This is a new color/size combination; composite a new image.
                spinner_image = WinImage.FromStream(
                    MemoryStream(
                        composite_gif_on_color(
                            str(Path(__file__).parent.parent / "resources/spinner.gif"),
                            background_color,
                            size,
                        )
                    )
                )
                self.SPINNER_CACHE[cache_key] = spinner_image

            self.native.Image = spinner_image

    def refresh(self):
        # A refresh will be invoked if the DPI on the widget changes.
        # Change the image *before* rehinting.
        self.set_spinner_image()
        super().refresh()

    def set_background_color(self, color):
        super().set_background_color(color)
        # A change in background color means we need to generate a new image.
        self.set_spinner_image()

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
        self.interface.intrinsic.width = self.SPINNER_SIZE
        self.interface.intrinsic.height = self.SPINNER_SIZE
