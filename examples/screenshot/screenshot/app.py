import asyncio
from datetime import date, time
from io import BytesIO

from PIL import Image

import toga
from toga.constants import CENTER, COLUMN
from toga.style import Pack

from .canvas import draw_tiberius

MAJOR_GENERAL = "\n".join(
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
)
JABBERWOCKY = "\n".join(
    [
        "'Twas brillig, and the slithy toves",
        "Did gyre and gimble in the wabe:",
        "All mimsy were the borogoves,",
        "And the mome raths outgrabe.",
        "",
        "“Beware the Jabberwock, my son!",
        "The jaws that bite, the claws that catch!",
        "Beware the Jubjub bird, and shun",
        "The frumious Bandersnatch!”",
        "",
        "He took his vorpal sword in hand;",
        "Long time the manxome foe he sought—",
        "So rested he by the Tumtum tree",
        "And stood awhile in thought.",
    ]
)


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
        canvas = toga.Canvas(style=Pack(padding=10, width=190, height=290))
        draw_tiberius(canvas)

        return toga.Box(children=[canvas], style=Pack(width=190, height=290))

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
            style=Pack(padding=10, width=450, height=300),
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
            value=MAJOR_GENERAL,
            style=Pack(padding=10, width=450, height=200),
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
            style=Pack(padding=10, width=450, height=200),
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
            style=Pack(padding=10, width=450, height=200),
        )
        tree.expand()
        return tree

    def create_webview(self):
        return toga.WebView(
            url="https://beeware.org",
            style=Pack(padding=10, width=450, height=300),
        )

    def create_optioncontainer(self):
        container = toga.OptionContainer(
            content=[
                (
                    "Penzance",
                    toga.MultilineTextInput(value=MAJOR_GENERAL),
                ),
                ("Pinafore", toga.Box()),
                ("Mikado", toga.Box()),
            ],
            style=Pack(padding=10, width=450, height=300),
        )

        return container

    def create_scrollcontainer(self):
        container = toga.ScrollContainer(
            content=toga.Box(
                children=[
                    toga.Label(f"{i} yak{'s' if i > 1 else ''}: {'yak '* i}")
                    for i in range(1, 50)
                ],
                style=Pack(direction=COLUMN),
            ),
            style=Pack(padding=10, width=450, height=300),
        )

        return container

    def create_splitcontainer(self):
        container = toga.SplitContainer(
            content=[
                toga.MultilineTextInput(value=MAJOR_GENERAL),
                toga.MultilineTextInput(value=JABBERWOCKY),
            ],
            style=Pack(padding=10, width=450, height=300),
        )

        return container

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
        ]:
            try:
                content = getattr(self.app, f"create_{content_type}")()
                if content:
                    self.main_window.content = toga.Box(
                        children=[content],
                        style=Pack(direction=COLUMN),
                    )
                    if content_type == "webview":
                        await asyncio.sleep(3)
                    else:
                        await asyncio.sleep(0.2)

                    image = Image.open(BytesIO(self.main_window._impl.get_image_data()))

                    print(self.main_window.content.layout.content_width, image.size)
                    cropped = image.resize(
                        (
                            int(self.main_window.content.layout.content_width),
                            int(self.main_window.content.layout.content_height),
                        )
                    ).crop(
                        (
                            0,
                            0,
                            content.layout.content_width + 20,
                            content.layout.content_height + 20,
                        )
                    )
                    cropped.save(
                        self.app.paths.data
                        / f"{content_type}-{toga.platform.current_platform}.png"
                    )

            except NotImplementedError:
                pass
        self.app.exit()

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Add the content on the main window
        self.main_window.content = toga.Box()

        # Show the main window
        self.main_window.show()

        self.add_background_task(self.sequence)


def main():
    return ScreenshotGeneratorApp(
        "Screenshot Generator", "org.beeware.widgets.screenshot"
    )


if __name__ == "__main__":
    app = main()
    app.main_loop()
