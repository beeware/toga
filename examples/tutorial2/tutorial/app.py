import toga
from colosseum import CSS


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


def build(app):
    left_container = toga.Table(['Hello', 'World'])

    left_container.insert(None, 'root1', 'value1')
    left_container.insert(None, 'root2', 'value2')
    left_container.insert(None, 'root3', 'value3')
    left_container.insert(1, 'root4', 'value4')

    for i in range(0, 100):
        left_container.insert(None, 'root%s' % (i+5), 'value%s' % (i+5))

    right_content = toga.Box(
        style=CSS(flex_direction='column', padding_top=50)
    )

    for b in range(0, 10):
        right_content.add(
            toga.Button(
                'Hello world %s' % b,
                on_press=button_handler,
                style=CSS(width=200, margin=20)
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
        icon='icons/brutus.icns',
        group=things
    )
    cmd1 = toga.Command(
        action1,
        label='Action 1',
        tooltip='Perform action 1',
        icon='icons/brutus.icns',
        group=things
    )
    cmd2 = toga.Command(
        action2,
        label='Action 2',
        tooltip='Perform action 2',
        icon=toga.TIBERIUS_ICON,
        group=things
    )
    cmd3 = toga.Command(
        action3,
        label='Action 3',
        tooltip='Perform action 3',
        shortcut='k',
        icon='icons/cricket-72.png'
    )

    def action4(widget):
        print ("CALLING Action 4")
        cmd3.enabled = not cmd3.enabled

    cmd4 = toga.Command(
        action4,
        label='Action 4',
        tooltip='Perform action 4',
        icon='icons/brutus.icns'
    )

    app.commands.add(cmd1, cmd3, cmd4, cmd0)
    app.main_window.toolbar.add(cmd1, cmd2, cmd3, cmd4)

    return split


def main():
    return toga.App('First App', 'org.pybee.helloworld', startup=build)
