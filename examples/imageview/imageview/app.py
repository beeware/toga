try:
    import PIL.Image
    import PIL.ImageDraw

    pil_present = True
except ImportError:
    pil_present = False

import toga
from toga.constants import CENTER, COLUMN


class ImageViewApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow()

        box = toga.Box(
            margin=10,
            align_items=CENTER,
            direction=COLUMN,
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

        # image from pathlib.Path object
        # same as the above image, just with a different argument type
        image_from_pathlib_path = toga.Image(
            self.paths.app / "resources/pride-brutus.png"
        )

        # Scale ONE of the width or height, and the aspect ratio should be retained.
        box.add(
            toga.ImageView(
                image_from_pathlib_path,
                width=72,
            )
        )
        box.add(
            toga.ImageView(
                image_from_pathlib_path,
                height=72,
            )
        )

        # Image path can also be provided directly to ImageView - relative path.
        # Scale BOTH of the width or height, and the aspect ratio should be overridden.
        box.add(
            toga.ImageView(
                toga.Image("resources/pride-brutus.png"),
                width=72,
                height=72,
            )
        )

        # Image path can also be provided directly to ImageView - pathlib.Path object.
        # Flex with unspecified cross axis size: aspect ratio should be retained.
        box.add(
            toga.ImageView(
                self.paths.app / "resources/pride-brutus.png",
                flex=1,
            )
        )

        # Flex with fixed cross axis size: aspect ratio should be retained.
        box.add(
            toga.ImageView(
                self.paths.app / "resources/pride-brutus.png",
                flex=1,
                width=150,
            )
        )

        if pil_present:
            # Generate an image using pillow
            img = PIL.Image.new("RGBA", size=(110, 30))
            d1 = PIL.ImageDraw.Draw(img)
            d1.text((20, 10), "Pillow image", fill="green")
            imageview_from_pil = toga.ImageView(
                img,
                height=72,
                background_color="lightgray",
            )
            box.add(imageview_from_pil)

        # An empty imageview.
        empty_imageview = toga.ImageView()
        box.add(empty_imageview)

        self.main_window.content = box
        self.main_window.show()


def main():
    return ImageViewApp("ImageView", "org.beeware.toga.examples.imageview")


if __name__ == "__main__":
    main().main_loop()
