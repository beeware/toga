import io

from PIL import Image, ImageDraw

import toga
from toga.style.pack import CENTER, COLUMN, Pack


class ImageViewApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow()

        box = toga.Box(
            style=Pack(
                padding=10,
                alignment=CENTER,
                direction=COLUMN,
            )
        )

        # image from relative path, specified as a string to load brutus.png from
        # the package.
        image_from_path = toga.Image("resources/pride-brutus.png")

        # First display the image at its intrinsic size.
        box.add(
            toga.ImageView(
                image_from_path,
            )
        )

        # Scale ONE of the width or height, and the aspect ratio should be retained.
        box.add(
            toga.ImageView(
                image_from_path,
                style=Pack(width=72),
            )
        )
        box.add(
            toga.ImageView(
                image_from_path,
                style=Pack(height=72),
            )
        )

        # image from pathlib.Path object
        # same as the above image, just with a different argument type
        image_from_pathlib_path = toga.Image(
            self.paths.app / "resources" / "pride-brutus.png"
        )

        # Scale BOTH of the width or height, and the aspect ratio should be overridden.
        box.add(
            toga.ImageView(
                image_from_pathlib_path,
                style=Pack(width=72, height=72),
            )
        )

        # Flex with unpecified cross axis size: aspect ratio should be retained.
        box.add(
            toga.ImageView(
                image_from_pathlib_path,
                style=Pack(flex=1),
            )
        )

        # Flex with fixed cross axis size: aspect ratio should be retained.
        box.add(
            toga.ImageView(
                image_from_pathlib_path,
                style=Pack(flex=1, width=150),
            )
        )

        # image from bytes
        # generate an image using pillow
        img = Image.new("RGBA", size=(110, 30))
        d1 = ImageDraw.Draw(img)
        d1.text((20, 10), "Pillow image", fill="green")
        # get png bytes
        buffer = io.BytesIO()
        img.save(buffer, format="png", compress_level=0)

        image_from_bytes = toga.Image(data=buffer.getvalue())
        imageview_from_bytes = toga.ImageView(
            image_from_bytes,
            style=Pack(height=72, background_color="lightgray"),
        )
        box.add(imageview_from_bytes)

        # An empty imageview.
        empty_imageview = toga.ImageView()
        box.add(empty_imageview)

        self.main_window.content = box
        self.main_window.show()


def main():
    return ImageViewApp("ImageView", "org.beeware.widgets.imageview")


if __name__ == "__main__":
    app = main()
    app.main_loop()
