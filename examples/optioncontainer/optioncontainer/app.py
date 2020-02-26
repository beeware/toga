import toga

from toga.style import Pack

from toga.style.pack import (
    COLUMN,
    ROW,
    CENTER,
    LEFT,
    RIGHT,
)

PADDING = 5


class TogaDemo(toga.App):

    def startup(self):
        """
        Main entry point for app.
        """

        # create the main window
        self.main_window = toga.MainWindow(self.name)

        # create optioncontainer
        self.option_container = toga.OptionContainer(on_select=self.option_container_handler)

        # add a number of options that contain buttons
        self.add_option_buttons()

        # uncomment this line to add more options to demonstrate the "more navigator" (iOS)
        # self.add_option_more()

        self.main_window.content = self.option_container

        # show the main window
        self.main_window.show()

    def add_option_buttons(self):
        """
        Add a set of buttons as an option to OptionController.
        """

        # use same labels as iOS Clock app as an example
        for opt_label in ['World Clock', 'Alarm', 'Bedtime', 'Stopwatch', 'Timer']:
            box = toga.Box(id=opt_label, style=Pack(direction=COLUMN, alignment=CENTER))

            # spacer
            box.add(toga.Box(style=Pack(flex=1)))

            for num in range(1, 10):
                but_label = '{}: {}'.format(opt_label, num)
                box.add(
                    toga.Button(
                        but_label,
                        on_press=self.button_handler,
                        style=Pack(padding=PADDING, alignment=CENTER),
                    )
                )

            # spacer
            box.add(toga.Box(style=Pack(flex=1)))

            self.option_container.add(opt_label, box)

    def add_option_more(self):
        """
        Add some more options to demonstrate the "more navigation controller" (iOS).
        """

        for opt_label in ['Apple', 'Banana', 'Cherry', 'Dewberry']:
            box = toga.Box(id=opt_label, style=Pack(direction=COLUMN, alignment=CENTER))

            # spacer
            box.add(toga.Box(style=Pack(flex=1)))

            for num in range(1, 10):
                sw_label = '{}: {}'.format(opt_label, num)
                box.add(
                    toga.Switch(
                        sw_label,
                        on_toggle=self.switch_handler,
                        style=Pack(padding=PADDING, alignment=CENTER),
                    )
                )

            # spacer
            box.add(toga.Box(style=Pack(flex=1)))

            self.option_container.add(opt_label, box)

    def option_container_handler(self, option_container, option=None, index=None):
        print('option container on select: option_container={!r}, '
              'option={!r}, option.id={!r}, index={!r}'
              ''.format(option_container, option, option.id, index))

    def button_handler(self, button):
        print('button press: {!r}'.format(button.label))

    def switch_handler(self, switch):
        state = ('off', 'on')[switch.is_on]
        print('switch {!r} state is now {!r}'.format(switch.label, state))


def main():
    return TogaDemo('Toga Demo', 'org.beeware.toga-demo')
