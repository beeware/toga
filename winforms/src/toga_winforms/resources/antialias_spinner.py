import io
from pathlib import Path

from PIL import Image, ImageSequence
from System.Drawing import Image as NetImage
from System.IO import MemoryStream


def _composite_gif_on_color(path: str, rgb_color: tuple) -> bytes:
    with Image.open(path) as original_gif:
        composited_frames = []
        durations = []

        for frame in ImageSequence.Iterator(original_gif):
            frame = frame.convert("RGBA")
            background = Image.new("RGBA", frame.size, rgb_color + (255,))
            composited = Image.alpha_composite(background, frame)
            composited = composited.resize(
                (composited.width // 2, composited.height // 2), Image.BILINEAR
            )
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
    if color not in cache:
        cache[color] = NetImage.FromStream(
            MemoryStream(
                _composite_gif_on_color(
                    str(Path(__file__).parent / "spinner.gif"), color
                )
            )
        )
    return cache[color]
