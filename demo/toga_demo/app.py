#!/usr/bin/env python

import os

import toga
from toga.style import Pack
from toga.constants import COLUMN


class TogaDemo(toga.App):

    def startup(self):
        # Create the main window
        self.main_window = toga.MainWindow(self.name)

        left_container = toga.OptionContainer()

        left_table = toga.Table(
            headings=['Hello', 'World'],
            data=[
                ('root1', 'value1'),
                ('root2', 'value2'),
                ('root3', 'value3'),
                ('root4', 'value4'),
            ]
        )

        left_tree = toga.Tree(
            headings=['Navigate'],
            data={
                ('root1',): {
                },
                ('root2',): {
                    ('root2.1',): None,
                    ('root2.2',): [
                        ('root2.2.1',),
                        ('root2.2.2',),
                        ('root2.2.3',),
                    ]
                }
            }
        )

        left_container.add('Table', left_table)
        left_container.add('Tree', left_tree)

        right_content = toga.Box(style=Pack(direction=COLUMN))
        for b in range(0, 10):
            right_content.add(
                toga.Button(
                    'Hello world %s' % b,
                    on_press=self.button_handler,
                    style=Pack(padding=20)
                )
            )

        right_container = toga.ScrollContainer()

        right_container.content = right_content

        split = toga.SplitContainer()

        split.content = [left_container, right_container]

        cmd1 = toga.Command(self.action1, 'Action 1', tooltip='Perform action 1', icon=os.path.join(os.path.dirname(__file__), 'icons/brutus-32.png'))
        cmd2 = toga.Command(self.action2, 'Action 2', tooltip='Perform action 2', icon=toga.Icon.TIBERIUS_ICON)

        self.main_window.toolbar.add(cmd1, cmd2)

        self.main_window.content = split

        # Show the main window
        self.main_window.show()

    def button_handler(self, widget):
        print("button press")
        for i in range(0, 10):
            yield 1
            print ('still running... (iteration %s)' % i)

    def action1(self, widget):
        self.main_window.info_dialog('Toga', 'THIS! IS! TOGA!!')

    def action2(self, widget):
        if self.main_window.question_dialog('Toga', 'Is this cool or what?'):
            self.main_window.info_dialog('Happiness', 'I know, right! :-)')
        else:
            self.main_window.info_dialog('Shucks...', "Well aren't you a spoilsport... :-(")


def main():
    return TogaDemo('Toga Demo', 'org.pybee.toga-demo')
