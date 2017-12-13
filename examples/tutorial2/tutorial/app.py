import toga
from toga.style.flow import *


def button_handler(widget):
    print('button handler')
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


def tableSelected(widget, row):
    print("selected row %s" % row)


class Tutorial2App(toga.App):
    def startup(self):
        # Window class
        #   Main window of the application with title and size
        self.main_window = toga.MainWindow(self.name, size=(640, 480))
        self.main_window.app = self

        list_data = []
        for i in range(0, 100):
            list_data.append(('root%s' % i, 'value%s' % i))

        left_container = toga.Table(['Hello', 'World'], data=list_data, on_select=tableSelected)

        right_content = toga.Box(
            style=Flow(direction=COLUMN, padding_top=50)
        )

        for b in range(0, 10):
            right_content.add(
                toga.Button(
                    'Hello world %s' % b,
                    on_press=button_handler,
                    style=Flow(width=200, padding=20)
                )
            )

        right_container = toga.ScrollContainer(horizontal=False)

        right_container.content = right_content

        split = toga.SplitContainer()

        split.content = [left_container, right_container]

        things = toga.Group('Things')

        cmd0 = toga.Command(
            action1,
            label='Action 0',
            tooltip='Perform action 0',
            icon=toga.Icon('icons/brutus.icns'),
            group=things
        )
        cmd1 = toga.Command(
            action1,
            label='Action 1',
            tooltip='Perform action 1',
            icon=toga.Icon('icons/brutus.icns'),
            group=things
        )
        cmd2 = toga.Command(
            action2,
            label='Action 2',
            tooltip='Perform action 2',
            icon=toga.Icon.TIBERIUS_ICON,
            group=things
        )
        cmd3 = toga.Command(
            action3,
            label='Action 3',
            tooltip='Perform action 3',
            shortcut='k',
            icon=toga.Icon('icons/cricket-72.png')
        )

        def action4(widget):
            print("CALLING Action 4")
            cmd3.enabled = not cmd3.enabled

        cmd4 = toga.Command(
            action4,
            label='Action 4',
            tooltip='Perform action 4',
            icon=toga.Icon('icons/brutus.icns'),
        )

        self.commands.add(cmd1, cmd3, cmd4, cmd0)
        self.main_window.toolbar.add(cmd1, cmd2, cmd3, cmd4)

        # Add the content on the main window
        self.main_window.content = split

        # Show the main window
        self.main_window.show()


def main():
    return Tutorial2App('Tutorial 2', 'org.pybee.tutorial2')
