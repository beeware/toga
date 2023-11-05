import toga


# Use a WindowlessApp as the base class, as we don't want
# a MainWindow for the app.
class ExampleStatusIconApp(toga.WindowlessApp):
    def do_stuff(self, widget, **kwargs):
        window = toga.Window(title="Stuff to do")
        window.content = toga.Box()
        window.show()

    def startup(self):
        # Declare 2 status icon groups
        status_1 = toga.Group(
            "status 1",
            icon="resources/status-icon.png",
            status_item=True,
        )
        status_2 = toga.Group(
            "status 2",
            status_item=True,
        )

        # Add commands to the status item groups.
        cmd1 = toga.Command(
            self.do_stuff,
            text="Action 1",
            tooltip="Perform action 1",
            group=status_1,
            order=1,
        )
        cmd2 = toga.Command(
            self.do_stuff,
            text="Action 2",
            tooltip="Perform action 2",
            group=status_1,
            order=3,
        )

        sub_menu = toga.Group("Sub Menu", parent=status_1, order=3)
        cmd3 = toga.Command(
            self.do_stuff,
            text="Action 3",
            tooltip="Perform action 3",
            group=sub_menu,
        )
        cmd4 = toga.Command(
            self.do_stuff,
            text="Action 4",
            tooltip="Perform action 4",
            group=sub_menu,
        )

        cmd5 = toga.Command(
            self.do_stuff,
            text="Action 5",
            tooltip="Perform action 5",
            group=status_2,
        )
        cmd6 = toga.Command(
            self.do_stuff,
            text="Action 6",
            tooltip="Perform action 6",
            group=status_2,
        )

        # Register the commands with the groups
        self.commands.add(cmd1, cmd2, cmd3, cmd4, cmd5, cmd6)


def main():
    return ExampleStatusIconApp("Status Icon App", "org.beeware.statusiconapp")


if __name__ == "__main__":
    app = main()
    app.main_loop()
