import toga
from toga.constants import COLUMN


class HardwareApp(toga.App):
    def startup(self):
        #############################################################
        # Camera
        #############################################################
        self.photo = toga.ImageView(
            image=toga.Image("resources/default.png"), width=200
        )

        camera_box = toga.Box(
            children=[
                toga.Box(
                    children=[
                        toga.Box(flex=1),
                        self.photo,
                        toga.Box(flex=1),
                    ]
                ),
                toga.Box(
                    children=[
                        # Take a fresh photo
                        toga.Button(
                            "Take Photo",
                            on_press=self.take_photo,
                            flex=1,
                            margin=5,
                        ),
                        # Select a photo from the photo library
                        # toga.Button(
                        #     "Select Photo",
                        #     on_press=self.select_photo,
                        #     flex=1,
                        #     margin=5,
                        # ),
                    ],
                ),
            ],
            direction=COLUMN,
            margin_bottom=20,
        )

        #############################################################
        # Location services
        #############################################################

        self.map_view = toga.MapView(flex=1)
        self.pin = None
        self.location.on_change = self.location_changed

        geo_box = toga.Box(
            children=[
                self.map_view,
                toga.Box(
                    children=[
                        toga.Button("Update", on_press=self.update_location, flex=1),
                        toga.Button(
                            "Start",
                            on_press=self.start_location_updates,
                            flex=1,
                        ),
                        toga.Button(
                            "Stop",
                            on_press=self.stop_location_updates,
                            flex=1,
                        ),
                        toga.Button(
                            "Background",
                            on_press=self.request_background_location,
                            flex=1,
                        ),
                    ],
                    margin=5,
                ),
            ],
            direction=COLUMN,
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
            if not self.camera.has_permission:
                await self.camera.request_permission()

            image = await self.camera.take_photo()
            if image is None:
                self.photo.image = "resources/default.png"
            else:
                self.photo.image = image
        except NotImplementedError:
            await self.main_window.dialog(
                toga.InfoDialog(
                    "Oh no!",
                    "The Camera API is not implemented on this platform",
                )
            )
        except PermissionError:
            await self.main_window.dialog(
                toga.InfoDialog(
                    "Oh no!",
                    "You have not granted permission to take photos",
                )
            )

    def location_changed(self, geo, location, altitude, **kwargs):
        self._set_location(location)

    def _set_location(self, location):
        self.map_view.location = location

        if self.pin is None:
            self.pin = toga.MapPin(location, title="Here!")
            self.map_view.pins.add(self.pin)
            self.map_view.zoom = 16
        else:
            self.pin.location = location

    async def update_location(self, widget, **kwargs):
        try:
            await self.location.request_permission()

            location = await self.location.current_location()
            self._set_location(location)

        except NotImplementedError:
            await self.main_window.dialog(
                toga.InfoDialog(
                    "Oh no!",
                    "The Location API is not implemented on this platform",
                )
            )
        except PermissionError:
            await self.main_window.dialog(
                toga.InfoDialog(
                    "Oh no!",
                    "You have not granted permission to track location",
                )
            )

    async def start_location_updates(self, widget, **kwargs):
        try:
            await self.location.request_permission()

            self.location.start_tracking()
        except NotImplementedError:
            await self.main_window.dialog(
                toga.InfoDialog(
                    "Oh no!",
                    "The Location API is not implemented on this platform",
                )
            )
        except PermissionError:
            await self.main_window.dialog(
                toga.InfoDialog(
                    "Oh no!",
                    "You have not granted permission to track location",
                )
            )

    async def stop_location_updates(self, widget, **kwargs):
        try:
            await self.location.request_permission()

            self.location.stop_tracking()
        except NotImplementedError:
            await self.main_window.dialog(
                toga.InfoDialog(
                    "Oh no!",
                    "The Location API is not implemented on this platform",
                )
            )
        except PermissionError:
            await self.main_window.dialog(
                toga.InfoDialog(
                    "Oh no!",
                    "You have not granted permission to track location",
                )
            )

    async def request_background_location(self, widget, **kwargs):
        try:
            if self.location.has_background_permission:
                await self.main_window.dialog(
                    toga.InfoDialog(
                        "All good!",
                        (
                            "Application has permission to perform background "
                            "location tracking"
                        ),
                    )
                )
            else:
                if not await self.location.request_permission():
                    await self.main_window.dialog(
                        toga.InfoDialog(
                            "Oh no!",
                            "You have not granted permission for location tracking",
                        )
                    )
                    return

                if not await self.location.request_background_permission():
                    await self.main_window.dialog(
                        toga.InfoDialog(
                            "Oh no!",
                            (
                                "You have not granted permission for background "
                                "location tracking"
                            ),
                        )
                    )
        except NotImplementedError:
            await self.main_window.dialog(
                toga.InfoDialog(
                    "Oh no!",
                    "The Location API is not implemented on this platform",
                )
            )


def main():
    return HardwareApp("Hardware", "org.beeware.toga.examples.hardware")


if __name__ == "__main__":
    main().main_loop()
