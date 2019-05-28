from random import choice

import toga
from toga.style import Pack
from toga.constants import ROW, COLUMN
from toga.sources import Source

bee_movies = [
    {'year': 2008, 'title': 'The Secret Life of Bees', 'rating': '7.3', 'genre': 'Drama'},
    {'year': 2007, 'title': 'Bee Movie', 'rating': '6.1', 'genre': 'Animation, Adventure, Comedy'},
    {'year': 1998, 'title': 'Bees', 'rating': '6.3', 'genre': 'Horror'},
    {'year': 2007, 'title': 'The Girl Who Swallowed Bees', 'rating': '7.5', 'genre': 'Short'},
    {'year': 1974, 'title': 'Birds Do It, Bees Do It', 'rating': '7.3', 'genre': 'Documentary'},
    {'year': 1998, 'title': 'Bees: A Life for the Queen', 'rating': '8.0', 'genre': 'TV Movie'},
    {'year': 1994, 'title': 'Bees in Paradise', 'rating': '5.4', 'genre': 'Comedy, Musical'},
    {'year': 1947, 'title': 'Keeper of the Bees', 'rating': '6.3', 'genre': 'Drama'}
]

class Movie:
    # A class to wrap individual
    def __init__(self, year, title, rating, genre):
        self.year = year
        self.title = title
        self.rating = rating
        self.genre = genre


class Decade:
    # A class to wrap
    def __init__(self, decade):
        self.decade = decade
        self._data = []

    # Display values for the decade in the tree.
    @property
    def year(self):
        return "{}0's".format(self.decade)

    # Methods required for the data source interface
    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def can_have_children(self):
        return True


class DecadeSource(Source):
    def __init__(self):
        super().__init__()
        self._decades = []

    def __len__(self):
        return len(self._decades)

    def __getitem__(self, index):
        return self._decades[index]

    def add(self, entry):
        decade = entry['year'] // 10
        try:
            decade_root = {
                root.decade: root
                for root in self._decades
            }[decade]
        except KeyError:
            decade_root = Decade(decade)
            self._decades.append(decade_root)
            self._decades.sort(key=lambda v: v.decade)
        movie = Movie(**entry)
        decade_root._data.append(movie)
        self._notify('insert', parent=decade_root, index=len(decade_root._data) - 1, item=movie)


class ExampleTreeSourceApp(toga.App):
    # Table callback functions
    def on_select_handler(self, widget, node):
        if node and hasattr(node, 'title'):
            self.label.text = 'You selected node: {}'.format(node.title)
        else:
            self.label.text = 'No row selected'

    # Button callback functions
    def insert_handler(self, widget, **kwargs):
        entry = choice(bee_movies)
        self.tree.data.add(entry)

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Label to show responses.
        self.label = toga.Label('Ready.')

        self.tree = toga.Tree(
            headings=['Year', 'Title', 'Rating', 'Genre'],
            data=DecadeSource(),
            on_select=self.on_select_handler,
            style=Pack(flex=1)
        )

        # Buttons
        btn_style = Pack(flex=1)
        btn_insert = toga.Button('Insert Row', on_press=self.insert_handler, style=btn_style)
        btn_box = toga.Box(children=[btn_insert], style=Pack(direction=ROW))

        # Outermost box
        outer_box = toga.Box(
            children=[btn_box, self.tree, self.label],
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
    return ExampleTreeSourceApp('Tree Source', 'org.beeware.widgets.tree_source')


if __name__ == '__main__':
    app = main()
    app.main_loop()
