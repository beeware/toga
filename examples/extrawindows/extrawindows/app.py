import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW

class ExampleExtraWindowsApp(toga.App):
    # Button callback functions
    def do_new(self, widget, **kwargs):
        window_name = 'Window ' + str(self.window_count)
        self.window_count += 1
        w = ExtraWindow()
        w.startup(window_name, self)
        self.add_window(window_name, w)
        w.show()
        self.update()

    def do_close(self, widget, **kwargs):
        '''Close a window, but only if a window is selected in the table.'''
        selection = self.table_open_windows.selection
        if selection == None:
            return
        window_name = selection.open_windows
        w = self.window(window_name)
        w.close()




    def update(self):
        '''Update what is displayed in the tables, and enable/disable some
        buttons as appropriate'''
        self.table_open_windows.data.clear()

        for window_id in self.windows:
            if window_id == 'main':
                continue

            self.table_open_windows.data.append(window_id)

        # enable/disable the top box buttons, for open windows
        if len(self.windows) == 1:
            # If just one window, the main window, there are no child
            # windows.
            self.btn_close.enabled = False
        else:
            self.btn_close.enabled = True


    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(self.name)

        # Buttons next to the open windows table
        btn_style = Pack(flex=1)
        self.btn_new = toga.Button('New Window', on_press=self.do_new, style=btn_style)
        self.btn_close = toga.Button('Close Window', on_press=self.do_close, style=btn_style)

        self.table_open_windows = toga.Table(['Open Windows'])

        # Outermost box
        box = toga.Box(
            children=[self.btn_new, self.btn_close, self.table_open_windows],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
            )
        )

        # Add the content on the main window
        self.main_window.content = box



        # Show the main window
        self.main_window.show()

        # A counter of how many child windows we've made.
        self.window_count = 1

        self.update()

class ExtraWindow(toga.Window):
    def startup(self, name, parent_app):
        self.parent = parent_app
        self.name = name
        window_index = int(name.split()[1])

        box = toga.Box()
        self.title=name
        l = toga.Label(name)
        box.add(l)
        self.content = box


    def on_close(self):
        super().on_close()
        self.parent.update()

def main():
    return ExampleExtraWindowsApp('Extra Windows', 'org.pybee.widgets.extrawindows')


if __name__ == '__main__':
    app = main()
    app.main_loop()
