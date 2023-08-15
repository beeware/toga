import toga
from toga.constants import CENTER, COLUMN, ROW, Direction
from toga.style import Pack


class ContentControls(toga.Box):
    def __init__(self, split, index):
        super().__init__(style=Pack(direction=ROW, flex=1))
        self.split = split
        self.index = index

        self.sw_content = toga.Switch("Content", value=True, on_change=self.on_change)
        self.sw_flexible = toga.Switch("Flexible", value=True, on_change=self.on_change)
        self.add(
            toga.Box(style=Pack(flex=1)),  # Spacer
            toga.Box(
                style=Pack(direction=COLUMN),
                children=[self.sw_content, self.sw_flexible],
            ),
            toga.Box(style=Pack(flex=1)),  # Spacer
        )
        self.on_change(None)

    def on_change(self, switch):
        self.sw_flexible.enabled = self.sw_content.value

        if self.sw_content.value:
            box = toga.Box(style=Pack(padding=10, background_color="cyan"))
            if not self.sw_flexible.value:
                box.style.update(width=100, height=100)
        else:
            box = None

        content = list(self.split.content)
        content[self.index] = box
        self.split.content = content


class SplitControls(toga.Box):
    def __init__(self, split):
        super().__init__(style=Pack(direction=COLUMN, alignment=CENTER, flex=1))
        self.split = split

        self.add(
            toga.Box(
                style=Pack(direction=ROW),
                children=[
                    toga.Button(25, on_press=self.on_position),
                    toga.Button(50, on_press=self.on_position),
                    toga.Button(75, on_press=self.on_position),
                ],
            ),
            toga.Box(
                style=Pack(direction=ROW),
                children=[
                    toga.Button("Direction", on_press=self.on_direction),
                ],
            ),
        )

    def on_position(self, button):
        percent = int(button.text)
        content = self.split.content
        self.split.content = ((content[0], percent), (content[1], 100 - percent))

    def on_direction(self, button):
        self.split.direction = (
            Direction.HORIZONTAL
            if self.split.direction == Direction.VERTICAL
            else Direction.VERTICAL
        )


class SplitContainerApp(toga.App):
    def startup(self):
        self.split = toga.SplitContainer(style=Pack(padding=10, flex=1))

        main_box = toga.Box(
            style=Pack(direction=COLUMN),
            children=[
                toga.Box(
                    style=Pack(direction=ROW),
                    children=[
                        ContentControls(self.split, 0),
                        SplitControls(self.split),
                        ContentControls(self.split, 1),
                    ],
                ),
                self.split,
            ],
        )

        self.main_window = toga.MainWindow(self.name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return SplitContainerApp("SplitContainer", "org.beeware.widgets.splitcontainer")


if __name__ == "__main__":
    app = main()
    app.main_loop()
