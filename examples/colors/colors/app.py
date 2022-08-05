
import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW
from travertino import colors


class ExamplecolorsApp(toga.App):

    def change_color_foreground(self, widget):
        if widget.id == 'reset':
            self.change_color(colors.BLACK, None)
        else:
            self.change_color(widget.id, None)

    def change_color_background(self, widget):
        if widget.id == 'reset':
            self.change_color(None, colors.TRANSPARENT)
        else:
            self.change_color(None, widget.id)

    def change_color_both(self, widget):
        self.change_color(self.color_selection.value, self.color_background_selection.value)

    def change_color(self, color, background_color):
        for x in self.widget_box.children:
            if isinstance(x, toga.Widget) and x not in self.ignore_list_widgets:
                if color:
                    x.style.color = color
                if background_color:
                    x.style.background_color = background_color

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name, size=(640, 640))

        # create widgets to test colors on
        button = toga.Button('This is a button')
        label = toga.Label('This is a Label')
        multiline_text_input = toga.MultilineTextInput(initial='This is a Multiline Text Input field!')
        number_input = toga.NumberInput(default=1337)
        password_input = toga.PasswordInput(initial='adminadmin')
        progress_bar = toga.ProgressBar(max=100, value=50, running=True)
        selection = toga.Selection(items=['item 1', 'item 2', 'item 3', 'item 4', 'item 5', 'item 6'])
        slider = toga.Slider()
        switch = toga.Switch('Switch')
        table = toga.Table(
            headings=['Heading 1', 'Heading 2'],
            data=[
                ('value 1', 'value 2'),
                ('value 1', 'value 2'),
                ('value 1', 'value 2'),
                ('value 1', 'value 2'),
                ('value 1', 'value 2'),
                ('value 1', 'value 2')
            ],
            missing_value='none'
        )
        text_input = toga.TextInput(initial='This is a Text input field!')
        scroll_container = toga.ScrollContainer(
            horizontal=True,
            vertical=True,
            style=Pack(direction=COLUMN, height=70, padding=20)
        )
        temp_box = toga.Box(
            children=[toga.Label('Scrollcontainer example! filled with labels.')],
            style=Pack(direction=COLUMN)
        )
        for x in range(20):
            temp_box.add(toga.Label('Label'))
        scroll_container.content = temp_box
        self.box_label = toga.Label('This is a Box:')
        box = toga.Box(style=Pack(height=50))

        self.widget_box = toga.Box(
            children=[
                button,
                label,
                multiline_text_input,
                number_input,
                password_input,
                progress_bar,
                selection,
                slider,
                switch,
                table,
                text_input,
                scroll_container,
                self.box_label,
                box
            ],
            style=Pack(direction=COLUMN, flex=2)
        )
        self.ignore_list_widgets = [
            self.box_label,
        ]

        # set small padding space between widgets
        for x in self.widget_box.children:
            if isinstance(x, toga.Widget) and x not in self.ignore_list_widgets:
                x.style.padding_top = 2

        # setup control box
        b_change_fcollor_r = toga.Button(
            'color: red', id=colors.RED, on_press=self.change_color_foreground)
        b_change_fcollor_g = toga.Button(
            'color: green', id=colors.GREEN, on_press=self.change_color_foreground)
        b_change_fcollor_b = toga.Button(
            'color: blue', id=colors.BLUE, on_press=self.change_color_foreground)
        b_change_fcollor_t = toga.Button(
            'color: transparent', id=colors.TRANSPARENT, on_press=self.change_color_foreground, enabled=False)
        b_change_fcollor_reset = toga.Button(
            'color: reset', id='reset', on_press=self.change_color_foreground)
        b_change_bcollor_r = toga.Button(
            'color: red', id=colors.RED, on_press=self.change_color_background)
        b_change_bcollor_g = toga.Button(
            'color: green', id=colors.GREEN, on_press=self.change_color_background)
        b_change_bcollor_b = toga.Button(
            'color: blue', id=colors.BLUE, on_press=self.change_color_background)
        b_change_bcollor_t = toga.Button(
            'color: transparent', id=colors.TRANSPARENT, on_press=self.change_color_background)
        b_change_bcollor_reset = toga.Button(
            'color: reset', id='reset', on_press=self.change_color_background)

        self.color_selection = toga.Selection(items=colors.NAMED_COLOR)
        self.color_selection.value = colors.BLUE
        self.color_background_selection = toga.Selection(items=colors.NAMED_COLOR)
        self.color_background_selection.value = colors.ORANGE
        button_changecollor = toga.Button('Change color', on_press=self.change_color_both)
        control_box = toga.Box(
            children=[
                toga.Label('Color selection:'),
                b_change_fcollor_r,
                b_change_fcollor_g,
                b_change_fcollor_b,
                b_change_fcollor_t,
                b_change_fcollor_reset,
                toga.Label(' '),
                toga.Label('Background color selection:'),
                b_change_bcollor_r,
                b_change_bcollor_g,
                b_change_bcollor_b,
                b_change_bcollor_t,
                b_change_bcollor_reset,
                toga.Label(' '),
                toga.Label('Color selection:'),
                self.color_selection,
                toga.Label(' '),
                toga.Label('Background color selection:'),
                self.color_background_selection,
                toga.Label(' '),
                button_changecollor
            ],
            style=Pack(direction=COLUMN, padding=30, flex=1)
        )

        # Outermost box
        outer_box = toga.Box(
            children=[self.widget_box, control_box],
            style=Pack(
                flex=1,
                direction=ROW,
                padding=10,
                background_color='lightgray'
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
