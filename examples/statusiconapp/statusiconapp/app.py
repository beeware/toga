import asyncio

import toga


class StatusIconApp(toga.App):
    def startup(self):
        # Set app to be a background app
        self.main_window = toga.App.BACKGROUND

        # Declare 3 status icons. The first two will have menus, but only the first will
        # have the standard commands. The third status icon is a bare icon.
        status_1 = toga.MenuStatusIcon(icon="resources/status-icon.png")
        self.status_icons.add(
            status_1,
            toga.MenuStatusIcon(id="second", text="Other icon"),
            toga.SimpleStatusIcon(icon="resources/blue.png", on_press=self.do_stuff),
        )

        # Create some commands that can be added to the first status icon.
        # A MenuStatusIcon is also a group, so the commands will appear in that group.
        cmd1 = toga.Command(
            self.do_stuff,
            text="Action 1",
            tooltip="Perform action 1",
            order=2,
            group=status_1,
        )
        # If a command *doesn't* define a group, and it's added as a status icon, it
        # will be added to the end of the first status icon that has been registered.
        cmd2 = toga.Command(
            self.do_stuff,
            text="Action 2",
            tooltip="Perform action 2",
            order=1,
        )

        # Create a submenu on the first status menu; the status icon
        # is the parent group.
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

        # Two commands for the second status icon. The status icon can be retrieved by
        # ID, and by index.
        cmd5 = toga.Command(
            self.do_stuff,
            text="Action 5",
            tooltip="Perform action 5",
            group=self.status_icons["second"],
        )
        cmd6 = toga.Command(
            self.do_stuff,
            text="Action 6",
            tooltip="Perform action 6",
            group=self.status_icons[1],
        )

        # Add the commands that will be part of status icons.
        self.status_icons.commands.add(cmd1, cmd2, cmd3, cmd4, cmd5, cmd6)

    async def on_running(self):
        # Once the app is running, start a heartbeat
        while True:
            await asyncio.sleep(1)
            print("Running...")

    def do_stuff(self, widget, **kwargs):
        window = toga.Window(title="Stuff to do")
        window.content = toga.Box()
        window.show()


def main():
    return StatusIconApp("Status Icon App", "org.beeware.toga.examples.statusiconapp")


if __name__ == "__main__":
    main().main_loop()
