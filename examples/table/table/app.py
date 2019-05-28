from random import choice

import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW

headings = ['Title', 'Year', 'Rating', 'Genre']
bee_movies = [
    ('The Secret Life of Bees', '2008', '7.3', 'Drama'),
    ('Bee Movie', '2007', '6.1', 'Animation, Adventure, Comedy'),
    ('Bees', '1998', '6.3', 'Horror'),
    ('The Girl Who Swallowed Bees', '2007', '7.5', 'Short'),
    ('Birds Do It, Bees Do It', '1974', '7.3', 'Documentary'),
    ('Bees: A Life for the Queen', '1998', '8.0', 'TV Movie'),
    ('Bees in Paradise', '1944', '5.4', 'Comedy, Musical'),
    ('Keeper of the Bees', '1947', '6.3', 'Drama')
]


class ExampleTableApp(toga.App):
    # Table callback functions
    def on_select_handler(self, widget, row, **kwargs):
        self.label.text = 'You selected row: {}'.format(row.title) if row is not None else 'No row selected'

    # Button callback functions
    def insert_handler(self, widget, **kwargs):
        self.table1.data.insert(0, *choice(bee_movies))

    def delete_handler(self, widget, **kwargs):
        if len(self.table1.data) > 0:
            self.table1.data.remove(self.table1.data[0])
        else:
            print('Table is empty!')

    def clear_handler(self, widget, **kwargs):
        self.table1.data.clear()

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        # Label to show which row is currently selected.
        self.label = toga.Label('Ready.')

        # Data to populate the table.
        data = []
        for x in range(5):
            data.append(tuple(str(x) for x in range(5)))

        self.table1 = toga.Table(
            headings=headings,
            data=bee_movies[:4],
            style=Pack(flex=1),
            on_select=self.on_select_handler
        )

        self.table2 = toga.Table(
            headings=headings,
            data=self.table1.data,
            style=Pack(flex=1)
        )

        tablebox = toga.Box(children=[self.table1, self.table2], style=Pack(flex=1))

        # Buttons
        btn_style = Pack(flex=1)
        btn_insert = toga.Button('Insert Row', on_press=self.insert_handler, style=btn_style)
        btn_delete = toga.Button('Delete Row', on_press=self.delete_handler, style=btn_style)
        btn_clear = toga.Button('Clear Table', on_press=self.clear_handler, style=btn_style)
        btn_box = toga.Box(children=[btn_insert, btn_delete, btn_clear], style=Pack(direction=ROW))

        # Most outer box
        outer_box = toga.Box(
            children=[btn_box, tablebox, self.label],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleTableApp('Table', 'org.beeware.widgets.table')


if __name__ == '__main__':
    app = main()
    app.main_loop()
