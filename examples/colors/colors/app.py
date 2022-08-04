
import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW
from travertino import colors

class ExamplecolorsApp(toga.App):

    def fChange_color(self, widget):
        for x in self.widget_box.children:
            if isinstance(x, toga.Widget) and not x in self.ignore_listWidgets: 
                x.style.color = self.ColorSelection.value
                x.style.background_color = self.ColorBackgroundSelection.value

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title = self.name, size = (640, 640))

        # create widgets to test colors on
        wButton = toga.Button('This is a button')
        wLabel = toga.Label('This is a Label')
        wMultilineTextInput = toga.MultilineTextInput(initial = 'This is a Multiline Text Input field!')
        wNumberInput = toga.NumberInput(default = 1337)
        wPasswordInput = toga.PasswordInput(initial = 'adminadmin')
        wProgressBar = toga.ProgressBar(max = 100, value = 50, running =  True)
        wSelection = toga.Selection(items = ['item 1', 'item 2', 'item 3', 'item 4', 'item 5', 'item 6'])
        wSlider = toga.Slider()
        wSwitch = toga.Switch('Switch')
        wTable = toga.Table(['Heading 1', 'Heading 2'])
        wTextInput = toga.TextInput(initial = 'This is a Text input field!')
        wScrollContainer = toga.ScrollContainer(horizontal = True, vertical = True, style = Pack(direction = COLUMN, height = 70, padding = 20))
        tempBox = toga.Box(
            children = [toga.Label('Scrollcontainer example! filled with labels.')],
            style = Pack(direction = COLUMN)
        )
        for x in range(20):
            tempBox.add(toga.Label('Label'))
        wScrollContainer.content = tempBox
        self.wBoxLabel = toga.Label('This is a Box:')
        wBox = toga.Box(style = Pack(height = 50) )

        self.widget_box = toga.Box(
            children = [
                wButton,
                wLabel,
                wMultilineTextInput,
                wNumberInput,
                wPasswordInput,
                wProgressBar,
                wSelection,
                wSlider,
                wSwitch,
                wTable,
                wTextInput,
                wScrollContainer,
                self.wBoxLabel,
                wBox
            ],
            style = Pack(direction = COLUMN, flex = 2)
        )
        self.ignore_listWidgets = [
            self.wBoxLabel,
        ]

        for x in self.widget_box.children:
            if isinstance(x, toga.Widget) and not x in self.ignore_listWidgets: 
                x.style.padding_top = 2

        #setup control box
        self.ColorSelection = toga.Selection(items = colors.NAMED_COLOR)
        self.ColorBackgroundSelection = toga.Selection(items = colors.NAMED_COLOR)
        button_Changecollor = toga.Button('Change color', on_press = self.fChange_color)
        control_box = toga.Box(
            children = [
                toga.Label('Color selection:'),
                self.ColorSelection,
                toga.Label(' '),
                toga.Label('Background color selection:'),
                self.ColorBackgroundSelection,
                toga.Label(' '),
                button_Changecollor
            ],
            style = Pack(direction = COLUMN, padding = 30, flex = 1)
        )

        # Outermost box
        outer_box = toga.Box(
            children = [self.widget_box, control_box],
            style = Pack(
                flex = 1,
                direction = ROW,
                padding = 10
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExamplecolorsApp('colors', 'org.beeware.widgets.colors')


if __name__ == '__main__':
    app = main()
    app.main_loop()
