import toga
from toga.constants import COLUMN
from toga.style import Pack


class ExampleHardwareApp(toga.App):
    def startup(self):
        try:
            # This will provide a prompt for camera permissions at startup.
            # If permission is denied, the app will continue.
            self.camera.request_photo_permission()
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
                        toga.Button(
                            "Take Photo",
                            on_press=self.take_photo,
                            style=Pack(flex=1, padding=5),
                        ),
                        toga.Button(
                            "Sync",
                            on_press=self.take_photo_sync,
                            style=Pack(flex=1, padding=5),
                        ),
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
            self.update_photo(None, image)
        except PermissionError:
            self.main_window.info_dialog(
                "Oh no!", "You have not granted permission to take photos"
            )

    def take_photo_sync(self, widget, **kwargs):
        try:
            self.camera.take_photo(on_result=self.update_photo)
        except PermissionError:
            self.main_window.info_dialog(
                "Oh no!", "You have not granted permission to take photos"
            )

    def update_photo(self, camera, image):
        # Set the photo to be the new image
        if image is None:
            self.photo.image = "resources/default.png"
        else:
            self.photo.image = image


def main():
    return ExampleHardwareApp("Hardware", "org.beeware.widgets.hardware")


if __name__ == "__main__":
    app = main()
    app.main_loop()
