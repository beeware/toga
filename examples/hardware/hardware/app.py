import toga
from toga.constants import COLUMN
from toga.style import Pack


class ExampleHardwareApp(toga.App):
    def startup(self):
        try:
            # This will provide a prompt for camera permissions at startup.
            # If permission is denied, the app will continue.
            self.camera.request_permission()
        except NotImplementedError:
            print("The Camera API is not implemented on this platform")

        self.photo = toga.ImageView(
            image=toga.Image("resources/default.png"), style=Pack(width=200)
        )

        main_box = toga.Box(
            children=[
                toga.Box(
                    children=[
                        toga.Box(style=Pack(flex=1)),
                        self.photo,
                        toga.Box(style=Pack(flex=1)),
                    ]
                ),
                toga.Box(
                    children=[
                        # Take a fresh photo
                        toga.Button(
                            "Take Photo",
                            on_press=self.take_photo,
                            style=Pack(flex=1, padding=5),
                        ),
                        # Select a photo from the photo library
                        # toga.Button(
                        #     "Select Photo",
                        #     on_press=self.select_photo,
                        #     style=Pack(flex=1, padding=5),
                        # ),
                    ],
                ),
            ],
            style=Pack(direction=COLUMN, padding_bottom=20),
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    async def take_photo(self, widget, **kwargs):
        try:
            image = await self.camera.take_photo()
            if image is None:
                self.photo.image = "resources/default.png"
            else:
                self.photo.image = image
        except PermissionError:
            await self.main_window.info_dialog(
                "Oh no!", "You have not granted permission to take photos"
            )


def main():
    return ExampleHardwareApp("Hardware", "org.beeware.examples.hardware")


if __name__ == "__main__":
    app = main()
    app.main_loop()
