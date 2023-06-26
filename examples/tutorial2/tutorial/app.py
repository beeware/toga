import toga
from toga.style.pack import COLUMN, Pack


def button_handler(widget):
    print("button handler")
    for i in range(0, 10):
        print("hello", i)
        yield 1
    print("done", i)


def action0(widget):
    print("action 0")


def action1(widget):
    print("action 1")


def action2(widget):
    print("action 2")


def action3(widget):
    print("action 3")


def action5(widget):
    print("action 5")


def action6(widget):
    print("action 6")


class Tutorial2App(toga.App):
    def startup(self):
        brutus_icon = "icons/brutus"
        cricket_icon = "icons/cricket-72.png"

        data = [("root%s" % i, "value %s" % i) for i in range(1, 100)]

        left_container = toga.Table(headings=["Hello", "World"], data=data)

        right_content = toga.Box(style=Pack(direction=COLUMN, padding_top=50))

        for b in range(0, 10):
            right_content.add(
                toga.Button(
                    "Hello world %s" % b,
                    on_press=button_handler,
                    style=Pack(width=200, padding=20),
                )
            )

        right_container = toga.ScrollContainer(horizontal=False)

        right_container.content = right_content

        split = toga.SplitContainer()

        # The content of the split container can be specified as a simple list:
        #    split.content = [left_container, right_container]
        # but you can also specify "weight" with each content item, which will
        # set an initial size of the columns to make a "heavy" column wider than
        # a narrower one. In this example, the right container will be twice
        # as wide as the left one.
        split.content = [(left_container, 1), (right_container, 2)]

        # Create a "Things" menu group to contain some of the commands.
        # No explicit ordering is provided on the group, so it will appear
        # after application-level menus, but *before* the Command group.
        # Items in the Things group are not explicitly ordered either, so they
        # will default to alphabetical ordering within the group.
        things = toga.Group("Things")
        cmd0 = toga.Command(
            action0,
            text="Action 0",
            tooltip="Perform action 0",
            icon=brutus_icon,
            group=things,
        )
        cmd1 = toga.Command(
            action1,
            text="Action 1",
            tooltip="Perform action 1",
            icon=brutus_icon,
            group=things,
        )
        cmd2 = toga.Command(
            action2,
            text="Action 2",
            tooltip="Perform action 2",
            icon=toga.Icon.TOGA_ICON,
            group=things,
        )

        # Commands without an explicit group end up in the "Commands" group.
        # The items have an explicit ordering that overrides the default
        # alphabetical ordering
        cmd3 = toga.Command(
            action3,
            text="Action 3",
            tooltip="Perform action 3",
            shortcut=toga.Key.MOD_1 + "k",
            icon=cricket_icon,
            order=3,
        )

        # Define a submenu inside the Commands group.
        # The submenu group has an order that places it in the parent menu.
        # The items have an explicit ordering that overrides the default
        # alphabetical ordering.
        sub_menu = toga.Group("Sub Menu", parent=toga.Group.COMMANDS, order=2)
        cmd5 = toga.Command(
            action5,
            text="Action 5",
            tooltip="Perform action 5",
            order=2,
            group=sub_menu,
        )
        cmd6 = toga.Command(
            action6,
            text="Action 6",
            tooltip="Perform action 6",
            order=1,
            group=sub_menu,
        )

        def action4(widget):
            print("CALLING Action 4")
            cmd3.enabled = not cmd3.enabled

        cmd4 = toga.Command(
            action4,
            text="Action 4",
            tooltip="Perform action 4",
            icon=brutus_icon,
            order=1,
        )

        # The order in which commands are added to the app or the toolbar won't
        # alter anything. Ordering is defined by the command definitions.
        self.commands.add(cmd1, cmd0, cmd6, cmd4, cmd5, cmd3)

        self.main_window = toga.MainWindow(title=self.name)
        self.main_window.toolbar.add(cmd1, cmd3, cmd2, cmd4)
        self.main_window.content = split

        self.main_window.show()


def main():
    return Tutorial2App("Tutorial 2", "org.beeware.helloworld")


if __name__ == "__main__":
    main().main_loop()
