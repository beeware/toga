from random import choice
import toga
from colosseum import CSS

headings = ['Title', 'Year', 'Rating', 'Genre']
bee_movies = [('The Secret Life of Bees', '2008', '7.3', 'Drama'),
              ('Bee Movie', '2007', '6.1', 'Animation, Adventure, Comedy'),
              ('Bees', '1998', '6.3', 'Horror'),
              ('The Girl Who Swallowed Bees', '2007', '7.5', 'Short'),
              ('Birds Do It, Bees Do It', '1974', '7.3', 'Documentary'),
              ('Bees: A Life for the Queen', '1998', '8.0', 'TV Movie'),
              ('Bees in Paradise', '1944', '5.4', 'Comedy, Musical'),
              ('Keeper of the Bees', '1947', '6.3', 'Drama')]

def build(app):
    # Label to show which row is currently selected.
    label = toga.Label('No row selected.')

    # Data to populate the table.
    data = []
    for x in range(5):
        data.append(tuple(str(x) for x in range(5)))

    def selection_handler(widget, row):
        label.text = 'You selected row: {}'.format(row) if row is not None else 'No row selected'

    table = toga.Table(headings=headings,
                       data=bee_movies[:4],
                       style=CSS(flex=1),
                       on_select=selection_handler)

    table2 = toga.Table(headings=headings,
                        data=table.data,
                        style=CSS(flex=1))

    tablebox = toga.Box(children=[table, table2], style=CSS(flex=1))

    # Button callback functions
    def insert_handler(widget):
        table.data.insert(0, choice(bee_movies))
        print('Nr of rows', len(table.data.data))

    def delete_handler(widget):
        if len(table.data.data) > 0:
            table.data.remove(table.data.data[0])
        else:
            print('Table is empty!')

    def clear_handler(widget):
        table.data.clear()

    # Buttons
    btn_style = CSS(flex=1)
    btn_insert = toga.Button('Insert Row', on_press=insert_handler, style=btn_style)
    btn_delete = toga.Button('Delete Row', on_press=delete_handler, style=btn_style)
    btn_clear = toga.Button('Clear Table', on_press=clear_handler, style=btn_style)
    btn_box = toga.Box(children=[btn_insert, btn_delete, btn_clear], style=CSS(flex_direction='row'))

    # Most outer box
    box = toga.Box(children=[tablebox, btn_box, label],
                   style=CSS(flex=1,
                             flex_direction='column',
                             padding=10,
                             min_width=500, min_height=300))
    return box


def main():
    return toga.App('Test Table', 'org.pybee.table', startup=build)


if __name__ == '__main__':
    app = main()
    app.main_loop()
