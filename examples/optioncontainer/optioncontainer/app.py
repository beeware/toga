import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class ExampleOptionContainerApp(toga.App):

    def _create_options(self):
        label_box0 = toga.Label('This is Box 0 ', style=Pack(padding=10))
        label_box1 = toga.Label('This is Box 1 ', style=Pack(padding=10))
        label_box2 = toga.Label('This is Box 2 ', style=Pack(padding=10))

        box0 = toga.Box(children=[label_box0])
        box1 = toga.Box(children=[label_box1])
        box2 = toga.Box(children=[label_box2])

        self.optioncontainer.add('Option 0', box0)
        self.optioncontainer.add('Option 1', box1)
        self.optioncontainer.add('Option 2', box2)
        self._refresh_select()

    def _refresh_select(self):
        items = []
        for i in range(len(self.optioncontainer.content)):
            items.append(str(i))
        self.select_option.items = items

    def on_add_option(self, button):
        self.optioncontainer.add('New Option', toga.Box())
        self._refresh_select()

    def on_enable_option(self, button):
        index = int(self.select_option.value)
        try:
            self.optioncontainer.content[index].enabled = not self.optioncontainer.content[index].enabled
        except toga.OptionContainer.OptionException as e:
            self.main_window.info_dialog('Oops', str(e))

    def on_change_option_title(self, button):
        index = int(self.select_option.value)
        self.optioncontainer.content[index].label = self.input_change_title.value

    def on_remove_option(self, button):
        try:
            index = int(self.select_option.value)
            del self.optioncontainer.content[index]
            self._refresh_select()
        except toga.OptionContainer.OptionException as e:
            self.main_window.info_dialog('Oops', str(e))

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # styles
        style_flex = Pack(flex=1, padding=5)
        style_row = Pack(direction=ROW, flex=1)
        style_select = Pack(direction=ROW, flex=1, padding_right=10)
        style_col = Pack(direction=COLUMN, flex=1)

        # select
        label_select = toga.Label('Select an Option position:', style=style_flex)
        self.select_option = toga.Selection(style=style_flex)
        # buttons
        btn_remove = toga.Button(
            'Remove',
            on_press=self.on_remove_option,
            style=style_flex
        )
        btn_enabled = toga.Button(
            'Toggle enabled',
            on_press=self.on_enable_option,
            style=style_flex
        )
        # change label
        self.input_change_title = toga.TextInput(style=style_flex)
        btn_change_title = toga.Button(
            'Change title',
            on_press=self.on_change_option_title,
            style=style_flex
        )

        box_select = toga.Box(
            style=style_select,
            children=[label_select, self.select_option]
        )
        box_actions_col1 = toga.Box(
            style=style_row,
            children=[btn_remove, btn_enabled]
        )
        box_actions_col2 = toga.Box(
            style=style_row,
            children=[self.input_change_title, btn_change_title]
        )
        box_actions = toga.Box(
            style=style_col,
            children=[box_actions_col1, box_actions_col2]
        )
        box_container_actions = toga.Box(
            style=style_row,
            children=[box_select, box_actions]
        )

        self.optioncontainer = toga.OptionContainer(style=Pack(padding_bottom=20))
        self._create_options()

        btn_add = toga.Button('Add Option', on_press=self.on_add_option)
        box_general_actions = toga.Box(
            style=Pack(padding_bottom=10),
            children=[btn_add]
        )

        # Outermost box
        outer_box = toga.Box(
            children=[
                box_general_actions,
                box_container_actions,
                self.optioncontainer
            ],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
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
