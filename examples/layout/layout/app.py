import toga
from toga.constants import CENTER, COLUMN, ROW, HIDDEN, VISIBLE
from toga.style import Pack


class ExampleLayoutApp(toga.App):

    def startup(self):

        self.button_hide = toga.Button(
            text='Hide label',
            style=Pack(padding=10, width=120),
            on_press=self.hide_label,
        )

        self.button_add = toga.Button(
            text='Add image',
            style=Pack(padding=10, width=120),
            on_press=self.add_image,
        )

        self.button_remove = toga.Button(
            text='Remove image',
            style=Pack(padding=10, width=120),
            on_press=self.remove_image,
            enabled=False,
        )

        self.button_insert = toga.Button(
            text='Insert image',
            style=Pack(padding=10, width=120),
            on_press=self.insert_image,
        )

        self.button_reparent = toga.Button(
            text='Reparent image',
            style=Pack(padding=10, width=120),
            on_press=self.reparent_image,
            enabled=False,
        )

        self.button_add_to_scroll = toga.Button(
            text='Add new label',
            style=Pack(padding=10, width=120),
            on_press=self.add_label,
        )

        self.content_box = toga.Box(children=[], style=Pack(direction=COLUMN, padding=10, flex=1))

        image = toga.Image('resources/tiberius.png')
        self.image_view = toga.ImageView(image, style=Pack(padding=10, width=60, height=60))

        # this tests adding children during init, before we have an implementation
        self.button_box = toga.Box(
            children=[
                self.button_hide,
                self.button_add,
                self.button_insert,
                self.button_reparent,
                self.button_remove,
                self.button_add_to_scroll,
            ],
            style=Pack(direction=COLUMN),
        )

        self.box = toga.Box(
            children=[],
            style=Pack(direction=ROW, padding=10, alignment=CENTER, flex=1)
        )

        # this tests adding children when we already have an impl but no window or app
        self.box.add(self.button_box)
        self.box.add(self.content_box)

        # add a couple of labels to get us started
        self.labels = []
        for i in range(3):
            self.add_label()

        self.main_window = toga.MainWindow()
        self.main_window.content = self.box
        self.main_window.show()

    def hide_label(self, sender):
        if self.labels[0].style.visibility == HIDDEN:
            self.labels[0].style.visibility = VISIBLE
            self.button_hide.text = "Hide label"
        else:
            self.labels[0].style.visibility = HIDDEN
            self.button_hide.text = "Show label"

    def add_image(self, sender):
        self.content_box.add(self.image_view)

        self.button_reparent.enabled = True
        self.button_remove.enabled = True
        self.button_add.enabled = False
        self.button_insert.enabled = False

    def insert_image(self, sender):
        self.content_box.insert(1, self.image_view)

        self.button_reparent.enabled = True
        self.button_remove.enabled = True
        self.button_add.enabled = False
        self.button_insert.enabled = False

    def remove_image(self, sender):
        self.image_view.parent.remove(self.image_view)

        self.button_reparent.enabled = False
        self.button_remove.enabled = False
        self.button_add.enabled = True
        self.button_insert.enabled = True

    def reparent_image(self, sender):
        if self.image_view.parent is self.button_box:
            self.content_box.insert(0, self.image_view)
        elif self.image_view.parent is self.content_box:
            self.button_box.add(self.image_view)

    def add_label(self, sender=None):
        # this tests adding children when we already have an impl, window and app
        new_label = toga.Label(
            'Label {}'.format(len(self.content_box.children)),
            style=Pack(padding=2, width=70)
        )
        self.content_box.add(new_label)
        self.labels.append(new_label)


def main():
    return ExampleLayoutApp('Layout', 'org.beeware.widgets.layout')


if __name__ == '__main__':
    app = main()
    app.main_loop()
