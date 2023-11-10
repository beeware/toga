import asyncio
from datetime import date, time
from io import BytesIO

from PIL import Image

import toga
from toga.constants import CENTER, COLUMN
from toga.style import Pack

from .canvas import draw_tiberius


class ScreenshotGeneratorApp(toga.App):
    def create_activityindicator(self):
        return toga.Box(
            children=[
                toga.Box(style=Pack(flex=1)),
                toga.ActivityIndicator(running=True, style=Pack(padding=10)),
                toga.Box(style=Pack(flex=1)),
            ],
            style=Pack(width=100),
        )

    def create_button(self):
        return toga.Box(
            children=[
                toga.Button(
                    "Launch rocket",
                    style=Pack(padding=10, flex=1),
                )
            ],
            style=Pack(width=300),
        )

    def create_canvas(self):
        canvas = toga.Canvas(style=Pack(padding=10, width=280, height=290))
        draw_tiberius(canvas)

        return toga.Box(children=[canvas], style=Pack(width=280, height=290))

    def create_dateinput(self):
        return toga.Box(
            children=[
                toga.Box(style=Pack(flex=1)),
                toga.DateInput(value=date(2014, 4, 21), style=Pack(padding=10)),
                toga.Box(style=Pack(flex=1)),
            ],
            style=Pack(width=300),
        )

    def create_detailedlist(self):
        brutus_icon = toga.Icon("resources/brutus.png")
        user_icon = toga.Icon("resources/user.png")
        return toga.DetailedList(
            data=[
                {
                    "icon": brutus_icon,
                    "title": "Brutus",
                    "subtitle": "Are you the very model of a modern major general?",
                },
                {
                    "icon": user_icon,
                    "title": "Major General",
                    "subtitle": "I have information animal, mineral, and vegetable...",
                },
                {
                    "icon": brutus_icon,
                    "title": "Brutus",
                    "subtitle": "Ah - but do you know the kings of England?",
                },
                {
                    "icon": user_icon,
                    "title": "Major General",
                    "subtitle": "I can quote the fights historical!",
                },
            ],
            style=Pack(padding=10, width=self.MAX_WIDTH, height=300),
        )

    def create_divider(self):
        return toga.Box(
            children=[
                toga.Label(
                    "I'm on top", style=Pack(flex=1, padding=5, text_align=CENTER)
                ),
                toga.Divider(direction=toga.Divider.HORIZONTAL, style=Pack(padding=5)),
                toga.Label(
                    "I'm below", style=Pack(flex=1, padding=5, text_align=CENTER)
                ),
            ],
            style=Pack(width=300, direction=COLUMN),
        )

    def create_label(self):
        return toga.Box(
            children=[
                toga.Label(
                    "Brutus was here!",
                    style=Pack(padding=10, text_align=CENTER, flex=1),
                )
            ],
            style=Pack(width=300),
        )

    def create_multilinetextinput(self):
        return toga.MultilineTextInput(
            value="\n".join(
                [
                    "I am the very model of a modern Major-General.",
                    "I've information animal, mineral, and vegetable.",
                    "I know the kings of England, and I quote the fights historical",
                    "From Marathon to Waterloo, in order categorical.",
                    "I'm very well acquainted, too, with matters mathematical,",
                    "I understand equations, both the simple and quadratical,",
                    "About binomial theorem I'm teeming with a lot o' news,",
                    "With many cheerful facts about the square of the hypotenuse.",
                    "",
                    "I'm very good at integral and differential calculus;",
                    "I know the scientific names of beings animalculous:",
                    "In short, in matters vegetable, animal, and mineral,",
                    "I am the very model of a modern Major-General.",
                ]
            ),
            style=Pack(padding=10, width=self.MAX_WIDTH, height=200),
        )

    def create_numberinput(self):
        return toga.Box(
            children=[
                toga.NumberInput(
                    value=2.71818,
                    step=0.00001,
                    style=Pack(padding=10, flex=1),
                )
            ],
            style=Pack(width=300),
        )

    def create_passwordinput(self):
        return toga.Box(
            children=[
                toga.PasswordInput(
                    value="secret",
                    style=Pack(padding=10, flex=1),
                )
            ],
            style=Pack(width=300),
        )

    def create_progressbar(self):
        return toga.Box(
            children=[
                toga.ProgressBar(
                    value=42,
                    max=100,
                    style=Pack(padding=10, flex=1),
                )
            ],
            style=Pack(width=300),
        )

    def create_selection(self):
        return toga.Box(
            children=[
                toga.Selection(
                    items=["Titanium", "Yttrium", "Yterbium"],
                    style=Pack(padding=10, flex=1),
                )
            ],
            style=Pack(width=300),
        )

    def create_slider(self):
        return toga.Box(
            children=[
                toga.Slider(
                    value=42,
                    max=100,
                    style=Pack(padding=10, flex=1),
                )
            ],
            style=Pack(width=300),
        )

    def create_switch(self):
        return toga.Box(
            children=[
                toga.Box(style=Pack(flex=1)),
                toga.Switch(
                    "Turbo",
                    value=True,
                    style=Pack(padding=10),
                ),
                toga.Box(style=Pack(flex=1)),
            ],
            style=Pack(width=150),
        )

    def create_table(self):
        return toga.Table(
            headings=["Name", "Age", "Planet"],
            data=[
                ("Arthur Dent", 42, "Earth"),
                ("Ford Prefect", 37, "Betelgeuse Five"),
                ("Tricia McMillan", 38, "Earth"),
                ("Slartibartfast", 1005, "Magrathea"),
            ],
            style=Pack(padding=10, width=self.MAX_WIDTH, height=200),
        )

    def create_textinput(self):
        return toga.Box(
            children=[
                toga.TextInput(
                    value="Brutus was here!",
                    style=Pack(padding=10, flex=1),
                )
            ],
            style=Pack(width=300),
        )

    def create_timeinput(self):
        return toga.Box(
            children=[
                toga.Box(style=Pack(flex=1)),
                toga.TimeInput(value=time(9, 7, 37), style=Pack(padding=10)),
                toga.Box(style=Pack(flex=1)),
            ],
            style=Pack(width=300),
        )

    def create_tree(self):
        tree = toga.Tree(
            headings=["Name", "Age", "Status"],
            data={
                "Earth": {
                    ("Arthur Dent", 42, "Anxious"): None,
                    ("Tricia McMillan", 38, "Overqualified"): None,
                },
                "Betelgeuse Five": {
                    ("Ford Prefect", 37, "Hoopy"): None,
                },
                "Magrathea": {
                    ("Slartibartfast", 1005, "Annoyed"): None,
                },
            },
            style=Pack(padding=10, width=self.MAX_WIDTH, height=200),
        )
        tree.expand()
        return tree

    def create_webview(self):
        return toga.WebView(
            url="https://beeware.org",
            style=Pack(padding=10, width=self.MAX_WIDTH, height=300),
        )

    def create_optioncontainer(self):
        container = toga.OptionContainer(
            content=[
                (
                    "Blue",
                    toga.Box(style=Pack(background_color="cornflowerblue")),
                ),
                ("Green", toga.Box()),
                ("Red", toga.Box()),
            ],
            style=Pack(padding=10, width=self.MAX_WIDTH, height=300),
        )

        return container

    def create_scrollcontainer(self):
        container = toga.ScrollContainer(
            content=toga.Box(
                children=[
                    toga.Box(
                        style=Pack(
                            background_color="cornflowerblue", width=900, height=600
                        )
                    ),
                ],
                style=Pack(direction=COLUMN),
            ),
            style=Pack(padding=10, width=self.MAX_WIDTH, height=300),
        )

        return container

    def create_splitcontainer(self):
        container = toga.SplitContainer(
            content=[
                toga.Box(style=Pack(background_color="goldenrod")),
                toga.Box(style=Pack(background_color="cornflowerblue")),
            ],
            style=Pack(padding=10, width=self.MAX_WIDTH, height=300),
        )

        return container

    def create_window(self):
        if toga.platform.current_platform in {"iOS", "android"}:
            return None

        return toga.Window(title="Toga", position=(800, 200), size=(300, 250))

    def create_main_window(self):
        # No widget to create
        return True

    async def manual_screenshot(self, content=None):
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        def proceed(button, **kwargs):
            future.set_result(True)

        proceed_button = toga.Button(
            "Done",
            on_press=proceed,
            style=Pack(padding=10),
        )

        if content:
            self.main_window.content = toga.Box(
                children=[
                    content,
                    toga.Box(style=Pack(flex=1)),
                    proceed_button,
                ],
                style=Pack(direction=COLUMN),
            )
        else:
            self.main_window.content = toga.Box()
        await future

    async def sequence(self, app, **kwargs):
        print(f"Saving screenshots to {self.app.paths.data}")
        self.app.paths.data.mkdir(parents=True, exist_ok=True)
        for content_type in [
            "activityindicator",
            "button",
            "canvas",
            "dateinput",
            "detailedlist",
            "divider",
            "label",
            "multilinetextinput",
            "numberinput",
            "passwordinput",
            "progressbar",
            "selection",
            "slider",
            "switch",
            "table",
            "textinput",
            "timeinput",
            "tree",
            "webview",
            "optioncontainer",
            "scrollcontainer",
            "splitcontainer",
            "window",
            "main_window",
        ]:
            try:
                content = getattr(self.app, f"create_{content_type}")()
                if content:
                    if content_type == "main_window":
                        # image = self.main_window.screen.as_image()
                        # cropped = image.crop(... crop to window size ...)
                        #
                        # TODO: Crop the desktop image, rather than use a manual screenshot
                        await self.main_window.info_dialog(
                            "Manual intervention",
                            "Screenshot the main window, and then quit the app.",
                        )
                        self.main_window.toolbar.add(self.command2, self.command1)
                        self.main_window.content = toga.Box()

                        cropped = None
                    elif content_type == "window":
                        content.show()

                        # image = self.main_window.screen.as_image()
                        # cropped = image.crop(... crop to window size ...)
                        #
                        # TODO: Crop the desktop image, rather than use a manual screenshot
                        await self.main_window.info_dialog(
                            "Manual intervention",
                            "Screenshot the secondary window, then press Done.",
                        )
                        await self.manual_screenshot(toga.Box())
                        cropped = None

                        content.close()

                    elif (
                        content_type == "webview"
                        and toga.platform.current_platform == "macOS"
                    ):
                        # Manual screenshot required on macOS because webviews aren't
                        # rendered directly on the Window.
                        await self.main_window.info_dialog(
                            "Manual intervention",
                            "Screenshot the web widget content, then press Done.",
                        )
                        await self.manual_screenshot(content)
                        cropped = None
                    else:
                        self.main_window.content = toga.Box(
                            children=[content],
                            style=Pack(direction=COLUMN),
                        )

                        await asyncio.sleep(
                            {
                                "webview": 4,
                            }.get(content_type, 2)
                        )
                        image = Image.open(BytesIO(self.main_window.as_image().data))

                        scale_x = (
                            image.size[0]
                            / self.main_window.content.layout.content_width
                        )
                        scale_y = (
                            image.size[1]
                            / self.main_window.content.layout.content_height
                        )

                        cropped = image.crop(
                            (
                                0,
                                0,
                                (content.layout.content_width + 20) * scale_x,
                                (content.layout.content_height + 20) * scale_y,
                            )
                        )

                    if cropped:
                        cropped.save(
                            self.app.paths.data
                            / f"{content_type}-{toga.platform.current_platform}.png"
                        )

            except NotImplementedError:
                pass

    def startup(self):
        if toga.platform.current_platform in {"iOS", "android"}:
            self.MAX_WIDTH = 370
        else:
            self.MAX_WIDTH = 450

        # Set up main window
        self.main_window = toga.MainWindow(title="My Application")

        self.command1 = toga.Command(
            lambda _: None,
            text="Twist",
            icon=toga.Icon.DEFAULT_ICON,
        )
        self.command2 = toga.Command(
            lambda _: None,
            text="Shout",
            icon="resources/brutus",
        )

        # Add the content on the main window
        self.main_window.content = toga.Box()

        # Show the main window
        self.main_window.show()

        self.add_background_task(self.sequence)


def main():
    return ScreenshotGeneratorApp("My Application", "org.beeware.widgets.screenshot")


if __name__ == "__main__":
    app = main()
    app.main_loop()
