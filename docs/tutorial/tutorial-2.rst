=====================================
You put the box inside another box...
=====================================

The biggest conceptual idea in Toga is constructing a constraint-based layout.
So, lets look at a more complex example, involving layouts, scrollers, and
containers inside other containers.:

.. image:: screenshots/tutorial-2.png

Here's the source code::

    from __future__ import print_function, unicode_literals, absolute_import

    import toga

    def button_handler(widget):
        print("hello")

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

        right_content = toga.Container()
        buttons = [
            toga.Button('Hello world %s' % b, on_press=button_handler)
            for b in range(0, 10)
        ]

        for i, button in enumerate(buttons):
            right_content.add(button)

            if i == 0:
                right_content.constrain(button.TOP == right_content.TOP + 50)
            else:
                right_content.constrain(button.TOP == buttons[i-1].BOTTOM + 50)
            right_content.constrain(button.LEADING == right_content.LEADING + 50)
            right_content.constrain(button.TRAILING + 50 == right_content.TRAILING)

        right_content.constrain(buttons[-1].BOTTOM + 50 < right_content.BOTTOM)

        right_container = toga.ScrollContainer()

        right_container.content = right_content

        split = toga.SplitContainer()

        split.content = [left_container, right_container]

        cmd1 = toga.Command(action1, 'Action 1', tooltip='Perform action 1', icon='icons/brutus.icns')
        cmd2 = toga.Command(action2, 'Action 2', tooltip='Perform action 2', icon=toga.TIBERIUS_ICON)
        cmd3 = toga.Command(action3, 'Action 3', tooltip='Perform action 3', icon='icons/brutus.icns')

        def action4(widget):
            print ("CALLING ACtion 4")
            cmd3.enabled = not cmd3.enabled

        cmd4 = toga.Command(action4, 'Action 4', tooltip='Perform action 4', icon='icons/brutus.icns')

        app.main_window.toolbar = [cmd1, toga.SEPARATOR, cmd2, toga.SPACER, cmd3, toga.EXPANDING_SPACER, cmd4]

        return split

    if __name__ == '__main__':
        app = toga.App('First App', 'org.pybee.helloworld', startup=build)

        app.main_loop()
