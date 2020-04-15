import toga
from toga.style import Pack
from toga.constants import COLUMN


class ExampleOptionContainerApp(toga.App):

    def on_enable(self, button):
        self.optioncontainer.content[0].enabled = not self.optioncontainer.content[0].enabled

    def on_change_label(self, button):
        self.optioncontainer.content[0].label = 'Now I have another label!'

    def on_remove(self, button):
        self.optioncontainer.remove(0)

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        self.optioncontainer = toga.OptionContainer()

        style_btn = Pack(padding_bottom=2)
        btn_toggle_1 = toga.Button('Toggle enabled first option', on_press=self.on_enable, style=style_btn)
        btn_change_label = toga.Button('Change label in first option', on_press=self.on_change_label, style=style_btn)
        btn_remove_option = toga.Button('Remove first tab', on_press=self.on_remove, style=style_btn)

        label_box1 = toga.Label('This is Box 1 ', style=Pack(padding=10))
        label_box2 = toga.Label('This is Box 2 ', style=Pack(padding=10))
        label_box3 = toga.Label('This is Box 3 ', style=Pack(padding=10))

        box1 = toga.Box(children=[label_box1])
        box2 = toga.Box(children=[label_box2])
        box3 = toga.Box(children=[label_box3])

        self.optioncontainer.add('Option1', box1)
        self.optioncontainer.add('Option2', box2)
        self.optioncontainer.add('Option3', box3)

        # Outermost box
        outer_box = toga.Box(
            children=[
                btn_toggle_1,
                btn_change_label, btn_remove_option,
                self.optioncontainer
            ],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
                width=500,
                height=300
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleOptionContainerApp('Option Container Example', 'org.beeware.widgets.optioncontainer')


if __name__ == '__main__':
    app = main()
    app.main_loop()
