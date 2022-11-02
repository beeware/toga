import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class ExampleTestCommandApp(toga.App):
    # Button callback functions
    def do_stuff(self, widget, **kwargs):
        self.textpanel.value += "Do stuff\n"

    def do_clear(self, widget, **kwargs):
        self.textpanel.value = ""

    def action0(self, widget):
        print("action 0")
        self.textpanel.value += "action 0\n"

    def action1(self, widget):
        print("action 1")
        self.textpanel.value += "action 1\n"

    def action2(self, widget):
        print("action 2")
        self.textpanel.value += "action 2\n"

    def action3(self, widget):
        print("action 3")
        self.textpanel.value += "action 3\n"

    def action5(self, widget):
        print("action 5")
        self.textpanel.value += "action 5\n"

    def action6(self, widget):
        print("action 6")
        self.textpanel.value += "action 6\n"

    def action7(self, widget):
        print("action 7")
        self.textpanel.value += "action 7\n"

    def startup(self):
        brutus_icon_256 = "resources/brutus-256"
        cricket_icon_256 = "resources/cricket-256"
        tiberius_icon_256 = "resources/tiberius-256"

        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Add commands
        print("adding commands")
        # Create a "Things" menu group to contain some of the commands.
        # No explicit ordering is provided on the group, so it will appear
        # after application-level menus, but *before* the Command group.
        # Items in the Things group are not explicitly ordered either, so they
        # will default to alphabetical ordering within the group.

        things = toga.Group("Things")
        cmd0 = toga.Command(
            self.action0,
            text="Action 0",
            tooltip="Perform action 0",
            icon=brutus_icon_256,
            group=things,
        )
        cmd1 = toga.Command(
            self.action1,
            text="Action 1",
            tooltip="Perform action 1",
            icon=brutus_icon_256,
            group=things,
        )
        cmd2 = toga.Command(
            self.action2,
            text="TB Action 2",
            tooltip="Perform toolbar action 2",
            icon=brutus_icon_256,
            group=things,
        )

        # Commands without an explicit group end up in the "Commands" group.
        # The items have an explicit ordering that overrides the default
        # alphabetical ordering
        cmd3 = toga.Command(
            self.action3,
            text="Action 3",
            tooltip="Perform action 3",
            shortcut=toga.Key.MOD_1 + "k",
            icon=cricket_icon_256,
            group=toga.Group.COMMANDS,
            order=4,
        )

        # Define a submenu inside the Commands group.
        # The submenu group has an order that places it in the parent menu.
        # The items have an explicit ordering that overrides the default
        # alphabetical ordering.
        sub_menu = toga.Group("Sub Menu", parent=toga.Group.COMMANDS, order=1)
        cmd5 = toga.Command(
            self.action5,
            text="TB Action 5",
            tooltip="Perform toolbar action 5",
            order=2,
            group=sub_menu,
        )  # there is deliberately no icon to show that a toolbar action also works with text
        cmd6 = toga.Command(
            self.action6,
            text="Action 6",
            tooltip="Perform action 6",
            order=1,
            icon=cricket_icon_256,
            group=sub_menu,
        )
        cmd7 = toga.Command(
            self.action7,
            text="TB action 7",
            tooltip="Perform toolbar action 7",
            order=30,
            icon=tiberius_icon_256,
            group=sub_menu,
        )

        def action4(widget):
            print("action 4")
            cmd3.enabled = not cmd3.enabled
            self.textpanel.value += "action 4\n"

        cmd4 = toga.Command(
            action4,
            text="Action 4",
            tooltip="Perform action 4",
            icon=brutus_icon_256,
            order=3,
        )

        # The order in which commands are added to the app or the toolbar won't
        # alter anything. Ordering is defined by the command definitions.
        self.app.commands.add(cmd1, cmd0, cmd6, cmd4, cmd3)
        self.app.main_window.toolbar.add(cmd2, cmd5, cmd7)

        # Buttons
        btn_style = Pack(flex=1)
        btn_do_stuff = toga.Button("Do stuff", on_press=self.do_stuff, style=btn_style)
        btn_clear = toga.Button("Clear", on_press=self.do_clear, style=btn_style)
        btn_box = toga.Box(
            children=[btn_do_stuff, btn_clear], style=Pack(direction=ROW)
        )

        self.textpanel = toga.MultilineTextInput(
            readonly=False, style=Pack(flex=1), placeholder="Ready."
        )

        # Outermost box
        outer_box = toga.Box(
            children=[btn_box, self.textpanel],
            style=Pack(flex=1, direction=COLUMN, padding=10),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    print("app.main")
    return ExampleTestCommandApp("Test Command", "org.beeware.widgets.command")


if __name__ == "__main__":
    app = main()
    app.main_loop()
