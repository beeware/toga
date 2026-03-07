import toga
from toga.constants import COLUMN
from toga.style.pack import Pack


class MainForm(toga.MainWindow):
    def __init__(self):
        super().__init__(self)

        self.title = "MouseWheel Parent Scroll Example"
        self.size = (400, 400)
        self.textboxes = []

        # Create a scrollable panel (acts like a ScrollContainer)
        panel = toga.Box(style=Pack(direction=COLUMN, flex=1, margin=10))
        scroll_container = toga.ScrollContainer(style=Pack(flex=1), content=panel)

        # Clicking the panel background removes focus from controls
        panel._impl.native.MouseDown += self.on_form_click

        # Add some labels to make the panel tall enough to scroll
        for i in range(10):
            label = toga.Label(text=f"Label {i}")
            panel.add(label)

        for i in range(3):
            textbox = toga.MultilineTextInput(height=120, width=300)
            self.textboxes.append(textbox)

            textbox.placeholder = (
                f"Textbox {i}\n"
                "Scroll here when focused.\n"
                "When not focused, the ScrollContainer will scroll."
            )
            panel.add(textbox)
        self.textboxes[1].readonly = True
        self.textboxes[1].value = "lorem ipsum\n" * 15

        # Add more controls below so scrolling becomes obvious
        for i in range(10, 20):
            label = toga.Label(text=f"Label {i}")
            panel.add(label)

        self.content = scroll_container

    # When clicking the panel background, remove focus from controls
    # This allows the mouse wheel to scroll the container instead
    def on_form_click(self, sender, event):
        self._impl.native.ActiveControl = None


class TestApp(toga.App):
    def startup(self):

        self.main_window = MainForm()
        self.main_window.show()


def main():
    return TestApp(formal_name="testapp", app_id="org.beeware")


if __name__ == "__main__":
    app = main()
    app.main_loop()
