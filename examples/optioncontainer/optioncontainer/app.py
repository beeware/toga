import toga
from toga.constants import COLUMN, ROW


class OptionContainerApp(toga.App):
    def _create_options(self):
        self._box_count = 0
        for _ in range(3):
            self.optioncontainer.content.append(*self._create_option())
        self._refresh_select()

    def _create_option(self):
        result = (
            f"Option {self._box_count}",
            toga.Box(
                background_color="cyan",
                margin=10,
                children=[toga.Label(f"This is Box {self._box_count}")],
            ),
        )
        self._box_count += 1
        return result

    def _refresh_select(self):
        items = []
        for i in range(len(self.optioncontainer.content)):
            items.append(str(i))
        self.select_option.items = items

    def on_add_option(self, button):
        self.optioncontainer.content.append(*self._create_option())
        self._refresh_select()

    def on_insert_option(self, button):
        index = self.optioncontainer.current_tab.index
        self.optioncontainer.content.insert(index, *self._create_option())
        self._refresh_select()

    async def on_enable_option(self, button):
        index = int(self.select_option.value)
        try:
            self.optioncontainer.content[
                index
            ].enabled = not self.optioncontainer.content[index].enabled
        except ValueError as e:
            await self.main_window.dialog(toga.InfoDialog("Oops", str(e)))

    def on_change_option_title(self, button):
        index = int(self.select_option.value)
        self.optioncontainer.content[index].text = self.input_change_title.value

    async def on_activate_option(self, button):
        try:
            index = int(self.select_option.value)
            self.optioncontainer.current_tab = index
        except ValueError as e:
            await self.main_window.dialog(toga.InfoDialog("Oops", str(e)))

    async def on_remove_option(self, button):
        try:
            index = int(self.select_option.value)
            del self.optioncontainer.content[index]
            self._refresh_select()
        except ValueError as e:
            await self.main_window.dialog(toga.InfoDialog("Oops", str(e)))

    def set_next_tab(self, widget):
        if (
            self.optioncontainer.current_tab.index
            < len(self.optioncontainer.content) - 1
        ):
            self.optioncontainer.current_tab = (
                self.optioncontainer.current_tab.index + 1
            )

    def set_previous_tab(self, widget):
        if self.optioncontainer.current_tab.index > 0:
            self.optioncontainer.current_tab = (
                self.optioncontainer.current_tab.index - 1
            )

    def on_select_tab(self, widget, **kwargs):
        self.selected_label.text = (
            f"Tab {widget.current_tab.index} has been chosen: {widget.current_tab.text}"
        )

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow()

        # styles
        style_flex = {"flex": 1, "margin": 5}

        # select
        label_select = toga.Label("Select an Option position:", **style_flex)
        self.select_option = toga.Selection(margin=5, width=50)
        # buttons
        btn_activate = toga.Button(
            "Activate", on_press=self.on_activate_option, **style_flex
        )
        btn_remove = toga.Button("Remove", on_press=self.on_remove_option, **style_flex)
        btn_enabled = toga.Button(
            "Toggle enabled", on_press=self.on_enable_option, **style_flex
        )
        # change title
        self.input_change_title = toga.TextInput(**style_flex)
        btn_change_title = toga.Button(
            "Change title", on_press=self.on_change_option_title, **style_flex
        )

        box_select = toga.Box(
            direction=ROW,
            margin_right=10,
            width=200,
            children=[label_select, self.select_option],
        )
        box_actions_1 = toga.Box(
            direction=ROW,
            children=[btn_activate, btn_remove, btn_enabled],
        )
        box_actions_2 = toga.Box(
            direction=ROW,
            children=[self.input_change_title, btn_change_title],
        )

        self.selected_label = toga.Label("")
        self.optioncontainer = toga.OptionContainer(
            on_select=self.on_select_tab, margin_bottom=20, flex=1
        )
        self._create_options()

        btn_add = toga.Button(
            "Append new option", margin=5, on_press=self.on_add_option
        )
        btn_insert = toga.Button(
            "Insert new option before active option",
            margin=5,
            on_press=self.on_insert_option,
        )
        box_general_actions = toga.Box(margin_bottom=10, children=[btn_add, btn_insert])

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
            flex=1,
            direction=COLUMN,
            margin=10,
        )

        self.commands.add(
            toga.Command(
                self.set_next_tab,
                "Next tab",
                shortcut=toga.Key.MOD_1 + toga.Key.RIGHT,
                group=toga.Group.COMMANDS,
                order=1,
            ),
            toga.Command(
                self.set_previous_tab,
                "Previous tab",
                shortcut=toga.Key.MOD_1 + toga.Key.LEFT,
                group=toga.Group.COMMANDS,
                order=1,
            ),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return OptionContainerApp(
        "Option Container Example", "org.beeware.toga.examples.optioncontainer"
    )


if __name__ == "__main__":
    main().main_loop()
