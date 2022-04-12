from random import choice

import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack

headings = ["Title", "Year", "Rating", "Genre"]
bee_movies = [
    ("The Secret Life of Bees", "2008", "7.3", "Drama"),
    ("Bee Movie", "2007", "6.1", "Animation, Adventure, Comedy"),
    ("Bees", "1998", "6.3", "Horror"),
    ("The Girl Who Swallowed Bees", "2007", "7.5", "Short"),
    ("Birds Do It, Bees Do It", "1974", "7.3", "Documentary"),
    ("Bees: A Life for the Queen", "1998", "8.0", "TV Movie"),
    ("Bees in Paradise", "1944", "5.4", "Comedy, Musical"),
    ("Keeper of the Bees", "1947", "6.3", "Drama"),
]


class ExampleTableApp(toga.App):
    lbl_fontsize = None

    # Table callback functions
    def on_select_handler1(self, widget, row, **kwargs):
        self.label_table1.text = (
            "You selected row: {}".format(row.title)
            if row is not None
            else "No row selected"
        )

    def on_select_handler2(self, widget, row, **kwargs):
        if self.table2.selection is not None:
            self.label_table2.text = "Rows selected: {}".format(
                len(self.table2.selection)
            )
        else:
            self.label_table2.text = "No row selected"

    # Button callback functions
    def insert_handler(self, widget, **kwargs):
        self.table1.data.insert(0, *choice(bee_movies))

    def delete_handler(self, widget, **kwargs):
        if self.table1.selection:
            self.table1.data.remove(self.table1.selection)
        elif len(self.table1.data) > 0:
            self.table1.data.remove(self.table1.data[0])
        else:
            print("Table is empty!")

    def clear_handler(self, widget, **kwargs):
        self.table1.data.clear()

    def reset_handler(self, widget, **kwargs):
        self.table1.data = bee_movies[3:]

    def toggle_handler(self, widget, **kwargs):
        try:
            # Try to delete the "genre" column by accessor.
            # If the column doesn't exist, this will raise a ValueError,
            # which means we need to add it.
            self.table1.remove_column("genre")
        except ValueError:
            # Add the genre column. We provide the column *title*,
            # which is automatically converted into the data accessor `genre`.
            # If the data accessor can't be determined from the column title,
            # you could manually specify the accessor here, too.
            self.table1.add_column("Genre")

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        # Label to show which row is currently selected.
        self.label_table1 = toga.Label("Ready.", style=Pack(flex=1, padding_right=5))
        self.label_table2 = toga.Label(
            "Try multiple row selection.", style=Pack(flex=1, padding_left=5)
        )
        labelbox = toga.Box(
            children=[self.label_table1, self.label_table2],
            style=Pack(flex=0, padding_top=5),
        )

        # Change font size
        lbl_fontlabel = toga.Label("Font size =")
        self.lbl_fontsize = toga.Label("10")
        btn_reduce_size = toga.Button(
            " - ", on_press=self.reduce_fontsize, style=Pack(width=40)
        )
        btn_increase_size = toga.Button(
            " + ", on_press=self.increase_fontsize, style=Pack(width=40)
        )
        font_box = toga.Box(
            children=[
                lbl_fontlabel,
                self.lbl_fontsize,
                btn_reduce_size,
                btn_increase_size,
            ],
            style=Pack(direction=ROW, padding_bottom=5),
        )

        # Data to populate the table.
        if toga.platform.current_platform == "android":
            # FIXME: beeware/toga#1392 - Android Table doesn't allow lots of content
            table_data = bee_movies
        else:
            table_data = bee_movies * 1000

        self.table1 = toga.Table(
            headings=headings,
            data=table_data,
            style=Pack(
                flex=1,
                padding_right=5,
                font_family="monospace",
                font_size=int(self.lbl_fontsize.text),
                font_style="italic",
            ),
            multiple_select=False,
            on_select=self.on_select_handler1,
        )

        self.table2 = toga.Table(
            headings=headings,
            data=self.table1.data,
            multiple_select=True,
            style=Pack(flex=1, padding_left=5),
            on_select=self.on_select_handler2,
        )

        tablebox = toga.Box(children=[self.table1, self.table2], style=Pack(flex=1))

        # Buttons
        btn_style = Pack(flex=1)
        btn_insert = toga.Button(
            "Insert Row", on_press=self.insert_handler, style=btn_style
        )
        btn_delete = toga.Button(
            "Delete Row", on_press=self.delete_handler, style=btn_style
        )
        btn_clear = toga.Button(
            "Clear Table", on_press=self.clear_handler, style=btn_style
        )
        btn_reset = toga.Button(
            "Reset Table", on_press=self.reset_handler, style=btn_style
        )
        btn_toggle = toga.Button(
            "Toggle Column", on_press=self.toggle_handler, style=btn_style
        )
        btn_box = toga.Box(
            children=[btn_insert, btn_delete, btn_clear, btn_reset, btn_toggle],
            style=Pack(direction=ROW, padding_bottom=5),
        )

        # Most outer box
        outer_box = toga.Box(
            children=[font_box, btn_box, tablebox, labelbox],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
            ),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()

    def reduce_fontsize(self, widget):
        font_size = int(self.lbl_fontsize.text) - 1
        self.lbl_fontsize.text = str(font_size)
        font = toga.Font("monospace", font_size, "italic")
        self.table1._impl.set_font(font)

    def increase_fontsize(self, widget):
        font_size = int(self.lbl_fontsize.text) + 1
        self.lbl_fontsize.text = str(font_size)
        font = toga.Font("monospace", font_size, "italic")
        self.table1._impl.set_font(font)


def main():
    return ExampleTableApp("Table", "org.beeware.widgets.table")


if __name__ == "__main__":
    app = main()
    app.main_loop()
