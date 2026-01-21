import asyncio
from unittest.mock import Mock

import toga


class ExampleDoc(toga.Document):
    description = "Example Document"
    extensions = ["testbed", "tbed"]

    def create(self):
        # Create the main window for the document.
        self.main_window = toga.DocumentWindow(
            doc=self,
            content=toga.Box(),
        )
        self._content = Mock()

    def read(self):
        if self.path.name == "broken.testbed":
            raise RuntimeError("Unable to load broken document")
        else:
            self._content.read(self.path)

    def write(self):
        self._content.write(self.path)


class ReadonlyDoc(toga.Document):
    description = "Read-only Document"
    extensions = ["other"]

    def create(self):
        # Create the main window for the document.
        self.main_window = toga.DocumentWindow(
            doc=self,
            content=toga.Box(),
        )
        self._content = Mock()

    def read(self):
        self._content.read(self.path)


class Testbed(toga.App):
    # Objects can be added to this list to avoid them being garbage collected in the
    # middle of the tests running. This is problematic, at least, for WebView (#2648).
    _gc_protector = []

    def startup(self):
        # Toga installs a custom task factory to ensure that a strong reference to
        # long-lived tasks is retained until the task completes. This task factory is
        # used to verify that the custom task factory has been installed.
        toga_task_factory = self.loop.get_task_factory()

        def task_factory(loop, coro, **kwargs):
            task = toga_task_factory(loop, coro, **kwargs)
            assert task in self._running_tasks, f"missing task reference for {task}"
            return task

        self.loop.set_task_factory(task_factory)

        # Set a default return code for the app, so that a value is
        # available if the app exits for a reason other than the test
        # suite exiting/crashing.
        self.returncode = -1

        # Commands exist on the app's lifecycle, and the app API isn't designed to deal
        # with destroying commands, so we create all the commands up front for the app
        # to use.

        self.cmd_action = Mock()
        # A command with everything, in a group
        group = toga.Group("Other")
        self.cmd1 = toga.Command(
            self.cmd_action,
            "Full command",
            icon=toga.Icon.DEFAULT_ICON,
            tooltip="A full command definition",
            shortcut=toga.Key.MOD_1 + "1",
            group=group,
        )
        # A command with no tooltip, in the default group, with a non-printable shortcut
        self.cmd2 = toga.Command(
            self.cmd_action,
            "No Tooltip",
            icon=toga.Icon.DEFAULT_ICON,
            shortcut=toga.Key.MOD_1 + toga.Key.DOWN,
        )
        # A command without an icon, in the default group
        self.cmd3 = toga.Command(
            self.cmd_action,
            "No Icon",
            tooltip="A command with no icon",
            shortcut=toga.Key.MOD_1 + "3",
        )
        # A command in another section.
        # Also exercises the handling of space as a shortcut key.
        self.cmd4 = toga.Command(
            self.cmd_action,
            "Sectioned",
            icon=toga.Icon.DEFAULT_ICON,
            shortcut=toga.Key.MOD_1 + " ",
            tooltip="I'm in another section",
            section=2,
        )
        # Submenus inside the "other" group
        subgroup1 = toga.Group("Submenu1", section=2, parent=group)
        subgroup1_1 = toga.Group("Submenu1 menu1", parent=subgroup1)
        subgroup2 = toga.Group("Submenu2", section=2, parent=group)

        # Items on submenu1
        # An item that is disabled by default
        self.disabled_cmd = toga.Command(
            self.cmd_action,
            "Disabled",
            enabled=False,
            group=subgroup1,
        )
        # An item that has no action
        self.no_action_cmd = toga.Command(None, "No Action", group=subgroup1)
        # An item deep in a menu
        self.deep_cmd = toga.Command(self.cmd_action, "Deep", group=subgroup1_1)

        # Items on submenu2
        self.cmd5 = toga.Command(self.cmd_action, "Jiggle", group=subgroup2)

        # Items on the main group after a submenu
        self.cmd6 = toga.Command(self.cmd_action, "Wiggle", group=group, section=2)

        # Add all the commands
        self.commands.add(
            self.cmd1,
            self.cmd2,
            self.cmd3,
            self.cmd4,
            self.disabled_cmd,
            self.no_action_cmd,
            self.deep_cmd,
            self.cmd5,
            self.cmd6,
            # Add a default Preferences menu item (with no action)
            # so that we can verify the command definition is valid.
            toga.Command.standard(self, toga.Command.PREFERENCES),
        )

        # Set up some status icons. This will raise warnings on mobile.
        self.status1 = toga.MenuStatusIcon(icon="resources/icons/red.png")
        self.status2 = toga.MenuStatusIcon(id="second", text="Other icon")
        self.status_button = toga.SimpleStatusIcon(
            id="button",
            icon="resources/icons/blue.png",
            on_press=self.cmd_action,
        )
        self.status_icons.add(
            self.status1,
            self.status2,
            self.status_button,
        )

        # Commands for the first status icon
        self.status_cmd1 = toga.Command(
            self.cmd_action,
            text="Action 1",
            tooltip="Perform action 1",
            group=self.status1,
        )
        # If a command *doesn't* define a group, and it's added as a status icon, it
        # will be added to the end of the first status icon that has been registered.
        self.status_cmd2 = toga.Command(
            self.cmd_action,
            text="Action 2",
            tooltip="Perform action 2",
        )

        # Create a submenu on the first status menu;
        # the status icon is the parent group.
        self.status1_sub_menu = toga.Group("Sub Menu", parent=self.status1, order=3)
        self.status_cmd3 = toga.Command(
            self.cmd_action,
            text="Action 3",
            tooltip="Perform action 3",
            group=self.status1_sub_menu,
        )
        self.status_cmd4 = toga.Command(
            self.cmd_action,
            text="Action 4",
            tooltip="Perform action 4",
            group=self.status1_sub_menu,
        )

        # Commands for the second status icon
        self.status_cmd5 = toga.Command(
            self.cmd_action,
            text="Action 5",
            tooltip="Perform action 5",
            group=self.status_icons["second"],
        )
        self.status_cmd6 = toga.Command(
            self.cmd_action,
            text="Action 6",
            tooltip="Perform action 6",
            group=self.status_icons[1],
        )

        # Add the commands that will be part of status icons.
        self.status_icons.commands.add(
            self.status_cmd1,
            self.status_cmd2,
            self.status_cmd3,
            self.status_cmd4,
            self.status_cmd5,
            self.status_cmd6,
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = toga.Box(
            children=[
                toga.Label("Did you forget to use --test?"),
            ]
        )
        self.main_window.show()

    async def on_running(self):
        # As soon as the app is running and the main window is visible, use the GUI
        # thread to set a flag that the test suite can use as permission to proceed.
        # The NoQA is warning about using sleep in a loop, which would be good advice
        # if there was an underlying Event that we could await - but there isn't.
        try:
            async with asyncio.timeout(10):
                while not self.main_window.visible:  # noqa: ASYNC110
                    await asyncio.sleep(0.05)
            self.is_visible = True
        except TimeoutError:
            # No extra handling required in the app. The test thread will fail after 5
            # seconds, killing the test suite.
            pass


def main(appname):
    return Testbed(
        app_name=appname,
        document_types=[ExampleDoc, ReadonlyDoc],
    )
