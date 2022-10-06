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

    def on_insert_option(self, button):
        index = self.optioncontainer.current_tab.index
        self.optioncontainer.content.insert(index, 'New Option', toga.Box())
        self._refresh_select()

    def on_enable_option(self, button):
        index = int(self.select_option.value)
        try:
            self.optioncontainer.content[index].enabled = not self.optioncontainer.content[index].enabled
        except toga.OptionContainer.OptionException as e:
            self.main_window.info_dialog('Oops', str(e))

    def on_change_option_title(self, button):
        index = int(self.select_option.value)
        self.optioncontainer.content[index].text = self.input_change_title.value

    def on_activate_option(self, button):
        try:
            index = int(self.select_option.value)
            self.optioncontainer.current_tab = index
        except toga.OptionContainer.OptionException as e:
            self.main_window.info_dialog('Oops', str(e))

    def on_remove_option(self, button):
        try:
            index = int(self.select_option.value)
            del self.optioncontainer.content[index]
            self._refresh_select()
        except toga.OptionContainer.OptionException as e:
            self.main_window.info_dialog('Oops', str(e))

    def set_next_tab(self, widget):
        if self.optioncontainer.current_tab.index < len(self.optioncontainer.content) - 1:
            self.optioncontainer.current_tab += 1

    def set_previous_tab(self, widget):
        if self.optioncontainer.current_tab.index > 0:
            self.optioncontainer.current_tab -= 1

    def on_select_tab(self, widget, option):
        self.selected_label.text = "Tab {} has been chosen: {}".format(
            option.index, option.text,
        )

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # styles
        style_flex = Pack(flex=1, padding=5)

        # select
        label_select = toga.Label('Select an Option position:', style=style_flex)
        self.select_option = toga.Selection(style=Pack(padding=5, width=50))
        # buttons
        btn_activate = toga.Button(
            'Activate',
            on_press=self.on_activate_option,
            style=style_flex
        )
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
        # change title
        self.input_change_title = toga.TextInput(style=style_flex)
        btn_change_title = toga.Button(
            'Change title',
            on_press=self.on_change_option_title,
            style=style_flex
        )

        box_select = toga.Box(
            style=Pack(direction=ROW, padding_right=10, width=200),
            children=[label_select, self.select_option]
        )
        box_actions_1 = toga.Box(
            style=Pack(direction=ROW, flex=1),
            children=[btn_activate, btn_remove, btn_enabled]
        )
        box_actions_2 = toga.Box(
            style=Pack(direction=ROW, flex=1),
            children=[self.input_change_title, btn_change_title]
        )

        self.selected_label = toga.Label("")
        self.optioncontainer = toga.OptionContainer(
            on_select=self.on_select_tab,
            style=Pack(padding_bottom=20)
        )
        self._create_options()

        btn_add = toga.Button('Append new option', style=Pack(padding=5), on_press=self.on_add_option)
        btn_insert = toga.Button(
            'Insert new option before active option', style=Pack(padding=5), on_press=self.on_insert_option
        )
        box_general_actions = toga.Box(
            style=Pack(padding_bottom=10),
            children=[btn_add, btn_insert]
        )

        # Outermost box
        outer_box = toga.Box(
            children=[
                box_general_actions,
                box_select,
                box_actions_1,
                box_actions_2,
                self.selected_label,
                self.optioncontainer,
            ],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
            )
        )

        self.commands.add(
            toga.Command(
                self.set_next_tab,
                "Next tab",
                shortcut=toga.Key.MOD_1 + toga.Key.RIGHT,
                group=toga.Group.COMMANDS,
                order=1
            ),
            toga.Command(
                self.set_previous_tab,
                "Previous tab",
                shortcut=toga.Key.MOD_1 + toga.Key.LEFT,
                group=toga.Group.COMMANDS,
                order=1
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
