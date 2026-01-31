import toga
import toga.platform
from toga.constants import CENTER, HIDDEN, VISIBLE

if toga.platform.current_platform == "iOS":
    import toga_iOS

    toga_iOS.ENABLE_LIQUID_GLASS_ADAPTATION = True

if toga.platform.current_platform == "macOS":
    import toga_cocoa

    toga_cocoa.ENABLE_LIQUID_GLASS_ADAPTATION = True


class LayoutApp(toga.App):
    def startup(self):
        self.button_hide = toga.Button(text="Hide label", on_press=self.hide_label)
        self.button_add = toga.Button(text="Add image", on_press=self.add_image)
        self.button_remove = toga.Button(
            text="Remove image", on_press=self.remove_image, enabled=False
        )
        self.button_insert = toga.Button(
            text="Insert image", on_press=self.insert_image
        )
        self.button_reparent = toga.Button(
            text="Reparent image", on_press=self.reparent_image, enabled=False
        )
        self.button_add_to_scroll = toga.Button(
            text="Add new label", on_press=self.add_label
        )

        self.content_box = toga.Column(children=[], gap=4)

        image = toga.Image("resources/tiberius.png")
        self.image_view = toga.ImageView(image, width=60, height=60)

        # this tests adding children during init, before we have an implementation
        self.button_box = toga.Column(
            children=[
                self.button_hide,
                self.button_add,
                self.button_insert,
                self.button_reparent,
                self.button_remove,
                self.button_add_to_scroll,
            ],
            width=120,
            gap=20,
        )

        self.row_box = toga.Row(
            children=[],
            margin=20,
            gap=20,
            align_items=CENTER,
            justify_content=CENTER,
            flex=1,
        )

        # This tests adding children when we already have an impl but no window or app.
        # Empty boxes are used to work around cross-axis alignment issue (#2213)
        self.row_box.add(toga.Row(flex=1))
        self.row_box.add(self.button_box)
        self.row_box.add(self.content_box)
        self.row_box.add(toga.Row(flex=1))

        self.box = toga.Column(
            children=[
                toga.ScrollContainer(
                    content=toga.Column(
                        children=[
                            toga.Box(
                                height=200,
                                background_color="cornflowerblue",
                            ),
                            toga.Label(
                                text="Hello World",
                                margin_top=20,
                            ),
                        ],
                    ),
                    horizontal=False,
                    height=200,
                ),
                self.row_box,
            ],
        )

        # add a couple of labels to get us started
        self.labels = []
        for _ in range(3):
            self.add_label()

        self.main_window = toga.MainWindow()
        self.main_window.content = self.box
        self.main_window.bleed_top = True
        self.main_window.show()

    def hide_label(self, sender):
        if self.labels[0].visibility == HIDDEN:
            self.labels[0].visibility = VISIBLE
            self.button_hide.text = "Hide label"
        else:
            self.labels[0].visibility = HIDDEN
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
        new_label = toga.Label(f"Label {len(self.content_box.children)}")
        self.content_box.add(new_label)
        self.labels.append(new_label)


def main():
    return LayoutApp("Layout", "org.beeware.toga.examples.layout")


if __name__ == "__main__":
    main().main_loop()
