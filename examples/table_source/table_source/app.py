from random import choice

import toga
from toga.style import Pack
from toga.constants import ROW, COLUMN
from toga.sources import Source

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


class Movie:
    # A class to wrap individual movies
    def __init__(self, title, year, rating, genre):
        self.year = int(year)
        self.title = title
        self.rating = float(rating)
        self.genre = genre


class MovieSource(Source):
    def __init__(self):
        super().__init__()
        self._movies = []

    def __len__(self):
        return len(self._movies)

    def __getitem__(self, index):
        return self._movies[index]

    def add(self, entry):
        movie = Movie(*entry)
        self._movies.append(movie)
        self._movies.sort(key=lambda m: m.year)
        self._notify('insert', index=len(self._movies) - 1, item=movie)

    def remove(self, index):
        item = self._movies[index]
        del self._movies[index]
        self._notify('remove', item=item)

    def clear(self):
        self._movies = []
        self._notify('clear')


class GoodMovieSource(Source):
    # A data source that piggy-backs on a MovieSource, but only
    # exposes *good* movies (rating > 7.5)
    def __init__(self, source):
        super().__init__()
        self._source = source
        self._source.add_listener(self)

    # Implement the filtering of the underlying data source
    def _filtered(self):
        return (m for m in self._source._movies if m.rating > 7.0)

    # Methods required by the ListSource interface
    def __len__(self):
        return len(list(self._filtered()))

    def __getitem__(self, index):
        return sorted(self._filtered(), key=lambda m: -m.rating)[index]

    # A listener that passes on all notifications
    def insert(self, index, item):
        self._notify('insert', index=index, item=item)

    def remove(self, item):
        self._notify('remove', item=item)

    def clear(self):
        self._notify('clear')


class ExampleTableSourceApp(toga.App):
    # Table callback functions
    def on_select_handler(self, widget, row, **kwargs):
        self.label.text = 'You selected row: {}'.format(row.title) if row is not None else 'No row selected'

    # Button callback functions
    def insert_handler(self, widget, **kwargs):
        self.table1.data.add(choice(bee_movies))

    def delete_handler(self, widget, **kwargs):
        if len(self.table1.data) > 0:
            self.table1.data.remove(0)
        else:
            print('Table is empty!')

    def clear_handler(self, widget, **kwargs):
        self.table1.data.clear()

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        # Label to show which row is currently selected.
        self.label = toga.Label('Ready.')

        # Create two tables with custom data sources; the data source
        # of the second reads from the first.
        # The headings are also in a different order.
        self.table1 = toga.Table(
            headings=['Year', 'Title', 'Rating', 'Genre'],
            data=MovieSource(),
            style=Pack(flex=1),
            on_select=self.on_select_handler
        )

        self.table2 = toga.Table(
            headings=['Rating', 'Title', 'Year', 'Genre'],
            data=GoodMovieSource(self.table1.data),
            style=Pack(flex=1)
        )

        # Populate the table
        for entry in bee_movies:
            self.table1.data.add(entry)

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
    return ExampleTableSourceApp('Table Source', 'org.beeware.widgets.table_source')


if __name__ == '__main__':
    app = main()
    app.main_loop()
