from random import choice

import toga
from toga.style import Pack
from toga.constants import ROW, COLUMN

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

class ExampleTreeApp(toga.App):
    # Table callback functions
    def on_select_handler(self, widget, node):
        if node is not None and node.title:
            self.label.text = 'You selected node: {}'.format(node.title)
        else:
            self.label.text = 'No node selected'

    # Button callback functions
    def insert_handler(self, widget, **kwargs):
        item = choice(bee_movies)
        if item['year'] >= 2000:
            root = self.decade_2000s
        elif item['year'] >= 1990:
            root = self.decade_1990s
        elif item['year'] >= 1980:
            root = self.decade_1980s
        elif item['year'] >= 1970:
            root = self.decade_1970s
        elif item['year'] >= 1960:
            root = self.decade_1960s
        elif item['year'] >= 1950:
            root = self.decade_1950s
        else:
            root = self.decade_1940s

        self.tree.data.append(root, **item)

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Label to show responses.
        self.label = toga.Label('Ready.')

        self.tree = toga.Tree(
            headings=['Year', 'Title', 'Rating', 'Genre'],
            on_select=self.on_select_handler,
            style=Pack(flex=1)
        )

        self.decade_1940s = self.tree.data.append(None, year='1940s', title='', rating='', genre='')
        self.decade_1950s = self.tree.data.append(None, year='1950s', title='', rating='', genre='')
        self.decade_1960s = self.tree.data.append(None, year='1960s', title='', rating='', genre='')
        self.decade_1970s = self.tree.data.append(None, year='1970s', title='', rating='', genre='')
        self.decade_1980s = self.tree.data.append(None, year='1980s', title='', rating='', genre='')
        self.decade_1990s = self.tree.data.append(None, year='1990s', title='', rating='', genre='')
        self.decade_2000s = self.tree.data.append(None, year='2000s', title='', rating='', genre='')

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
    return ExampleTreeApp('Tree', 'org.beeware.widgets.tree')


if __name__ == '__main__':
    app = main()
    app.main_loop()
