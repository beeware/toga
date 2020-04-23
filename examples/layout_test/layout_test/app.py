import toga
from toga.style import Pack
from toga.constants import ROW, COLUMN, CENTER, BLUE


class ExampleBoxApp(toga.App):

    def startup(self):

        self.button_add = toga.Button(
            label='Add image',
            style=Pack(padding=10, width=120),
            on_press=self.add_image,
        )

        self.button_remove = toga.Button(
            label='Remove image',
            style=Pack(padding=10, width=120),
            on_press=self.remove_image,
        )

        self.button_insert = toga.Button(
            label='Insert image',
            style=Pack(padding=10, width=120),
            on_press=self.insert_image,
        )

        self.button_add_to_scroll = toga.Button(
            label='Add new label',
            style=Pack(padding=10, width=120),
            on_press=self.add_label,
        )

        self.scroll_box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1, color=BLUE))
        self.scroll_view = toga.ScrollContainer(content=self.scroll_box, style=Pack(width=120))

        icon = toga.Icon('')
        self.image_view = toga.ImageView(icon, style=Pack(padding=10, width=120, height=120))

        self.button_box = toga.Box(
            children=[
                self.button_add,
                self.button_remove,
                self.button_insert,
                self.button_add_to_scroll,
            ],
            style=Pack(direction=COLUMN),
        )

        self.box = toga.Box(
            children=[self.button_box, self.scroll_view],
            style=Pack(direction=ROW, padding=10, alignment=CENTER, flex=1)
        )

        self.main_window = toga.MainWindow()
        self.main_window.content = self.box
        self.main_window.show()

    def add_image(self, sender):
        self.button_box.add(self.image_view)

    def insert_image(self, sender):
        self.button_box.insert(1, self.image_view)

    def remove_image(self, sender):
        self.button_box.remove(self.image_view)

    def add_label(self, sender):
        new_label = toga.Label(
            'Label {}'.format(len(self.scroll_box.children)),
            style=Pack(padding=2, width=70)
        )
        self.scroll_box.add(new_label)


def main():
    return ExampleBoxApp('Layout Test', 'org.beeware.widgets.layout_test')


if __name__ == '__main__':
    app = main()
    app.main_loop()
