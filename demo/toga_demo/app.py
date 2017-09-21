#!/usr/bin/env python

import os
import toga
from colosseum import CSS


class TogaDemo(toga.App):

    def startup(self):
        # Create the main window
        self.main_window = toga.MainWindow(self.name)
        self.main_window.app = self

        left_container = toga.OptionContainer()

        left_table = toga.Table(['Hello', 'World'])

        left_table.insert(None, 'root1', 'value1')
        left_table.insert(None, 'root2', 'value2')
        left_table.insert(None, 'root3', 'value3')
        left_table.insert(1, 'root4', 'value4')

        left_tree = toga.Tree(['Navigate'])

        left_tree.insert(None, None, 'root1')

        root2 = left_tree.insert(None, None, 'root2')

        left_tree.insert(root2, None, 'root2.1')
        root2_2 = left_tree.insert(root2, None, 'root2.2')

        left_tree.insert(root2_2, None, 'root2.2.1')
        left_tree.insert(root2_2, None, 'root2.2.2')
        left_tree.insert(root2_2, None, 'root2.2.3')

        left_container.add('Table', left_table)
        left_container.add('Tree', left_tree)

        right_content = toga.Box()
        for b in range(0, 10):
            right_content.add(toga.Button('Hello world %s' % b, on_press=self.button_handler, style=CSS(margin=20)))

        right_container = toga.ScrollContainer()

        right_container.content = right_content

        split = toga.SplitContainer()

        split.content = [left_container, right_container]

        cmd1 = toga.Command(self.action1, 'Action 1', tooltip='Perform action 1', icon=os.path.join(os.path.dirname(__file__), 'icons/brutus-32.png'))
        cmd2 = toga.Command(self.action2, 'Action 2', tooltip='Perform action 2', icon=toga.TIBERIUS_ICON)

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
