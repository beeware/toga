import toga
from toga.constants import CENTER
from toga.style import Pack


class ExampleDatePickerApp(toga.App):
    
    def changed_date(self,  _, value):
        print(value)

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Add the content on the main window
        self.main_window.content = toga.Box(children=[toga.DatePicker(initial=None, on_change=self.changed_date, min_date="2021-01-01", max_date="2022-02-01")], style=Pack(alignment=CENTER))

        # Show the main window
        self.main_window.show()


def main():
    return ExampleDatePickerApp('Date Picker Example', 'org.beeware.widgets.datepicker')


if __name__ == '__main__':
    app = main()
    app.main_loop()
