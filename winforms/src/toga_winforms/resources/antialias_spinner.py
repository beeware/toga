import ctypes
import io
from pathlib import Path

from PIL import Image, ImageSequence
from System.Drawing import Image as NetImage
from System.IO import MemoryStream


def _get_size(logical_width=32, logical_height=32):
    user32 = ctypes.windll.user32
    try:
        user32.SetProcessDPIAware()
        dpi = user32.GetDpiForSystem()
    except AttributeError:  # pragma: no cover
        dpi = 96
    physical_width = logical_width * dpi / 96
    physical_height = logical_height * dpi / 96
    return int(physical_width * 2.5), int(
        physical_height * 2.5
    )  # *2 to make it sharp on monitor


def _composite_gif_on_color(path: str, rgb_color: tuple, size: tuple) -> bytes:
    with Image.open(path) as original_gif:
        composited_frames = []
        durations = []

        for frame in ImageSequence.Iterator(original_gif):
            frame = frame.convert("RGBA")
            background = Image.new("RGBA", frame.size, rgb_color + (255,))
            composited = Image.alpha_composite(background, frame)
            composited = composited.resize(size, Image.BILINEAR)
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
    size = _get_size()
    if (color, size) not in cache:
        cache[(color, size)] = NetImage.FromStream(
            MemoryStream(
                _composite_gif_on_color(
                    str(Path(__file__).parent / "spinner.gif"), color, size
                )
            )
        )
    return cache[(color, size)]
