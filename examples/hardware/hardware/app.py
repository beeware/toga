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

        try:
            # This will provide a prompt for geolocation permissions at startup.
            # If permission is denied, the app will continue.
            self.geolocation.request_permission()
        except NotImplementedError:
            print("The Geolocation API is not implemented on this platform")

        #############################################################
        # Camera
        #############################################################
        self.photo = toga.ImageView(
            image=toga.Image("resources/default.png"), style=Pack(width=200)
        )

        camera_box = toga.Box(
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

        #############################################################
        # Geolocation
        #############################################################

        self.map_view = toga.MapView(style=Pack(flex=1))
        self.pin = None
        self.geolocation.on_change = self.location_changed

        geo_box = toga.Box(
            children=[
                self.map_view,
                toga.Box(
                    children=[
                        toga.Button(
                            "Update", on_press=self.update_location, style=Pack(flex=1)
                        ),
                        toga.Button(
                            "Start",
                            on_press=self.start_location_updates,
                            style=Pack(flex=1),
                        ),
                        toga.Button(
                            "Stop",
                            on_press=self.stop_location_updates,
                            style=Pack(flex=1),
                        ),
                    ],
                    style=Pack(padding=5),
                ),
            ],
            style=Pack(direction=COLUMN),
        )

        #############################################################
        # Main app
        #############################################################

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = toga.OptionContainer(
            content=[
                toga.OptionItem("Camera", camera_box),
                toga.OptionItem("Geo", geo_box),
            ]
        )
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

    def location_changed(self, geo, location, altitude, **kwargs):
        print("APPLY LOCATION CHANGE")
        self.map_view.zoom = 16
        self.map_view.location = location

        if self.pin is None:
            self.pin = toga.MapPin(location, title="Here!")
            self.map_view.pins.add(self.pin)
        else:
            self.pin.location = location

    async def update_location(self, widget, **kwargs):
        print("Request location update")
        location = await self.geolocation.current_location
        print("GOT LOCATION", location)
        self.location_changed(None, location, None)

    def start_location_updates(self, widget, **kwargs):
        print("START LOCATION UPDATES")
        self.geolocation.start()

    def stop_location_updates(self, widget, **kwargs):
        print("STOP LOCATION UPDATES")
        self.geolocation.stop()


def main():
    return ExampleHardwareApp("Hardware", "org.beeware.examples.hardware")


if __name__ == "__main__":
    app = main()
    app.main_loop()
