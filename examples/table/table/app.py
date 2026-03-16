import random

import toga
from toga.constants import COLUMN, ROW


class TableApp(toga.App):
    def load_data(self):
        yak = toga.Icon.DEFAULT_ICON
        red = toga.Icon("icons/red")
        green = toga.Icon("icons/green")

        # Include some non-string objects to make sure conversion works correctly.
        self.bee_movies = [
            ((yak, "The Secret Life of Bees"), 2008, (green, 7.3), "Drama"),
            ((None, "Bee Movie"), 2007, (red, 6.1), "Animation, Adventure"),
            ((None, "Bees"), 1998, (red, 6.3), "Horror"),
            ((None, "Despicable Bee"), 2010, (green, 7.5)),  # Missing genre
            ((None, "Birds Do It, Bees Do It"), 1974, (green, 7.3), "Documentary"),
            ((None, "Bees: A Life for the Queen"), 1998, (green, 8.0), "TV Movie"),
            ((None, "Bees in Paradise"), 1944, (red, 5.4), None),  # None genre
            ((yak, "Keeper of the Bees"), 1947, (red, 6.3), "Drama"),
        ]
        self.initial_data = self.bee_movies * 10

    # Table callback functions
    def on_select_handler(self, widget, **kwargs):
        if selection := self.table.selection:
            number = len(selection)
            titles = ", ".join(row.title[1] for row in selection[:3])
            self.selection_label.text = (
                f"Rows selected: {number} ({titles}{'...' if number > 3 else ''})"
            )
            self.btn_delete.enabled = True
            self.btn_insert.text = "Insert random row before selection"
        else:
            self.selection_label.text = "No rows selected"
            self.btn_delete.enabled = False
            self.btn_insert.text = "Insert random row at top"

    async def on_activate(self, widget, row, **kwargs):
        adjective = random.choice(
            ["magnificent", "amazing", "awesome", "life-changing"]
        )
        genre = (getattr(row, "genre", "") or "no-genre").lower()
        msg = f"You selected the {adjective} {genre} movie {row.title[1]} ({row.year})"

        await self.main_window.dialog(
            toga.InfoDialog(
                title="movie selection",
                message=msg,
            )
        )

    # Button callback functions
    def insert_handler(self, widget, **kwargs):
        if selection := self.table.selection:
            index = self.table.data.index(selection[0])
        else:
            index = 0
        self.table.data.insert(index, random.choice(self.bee_movies))

    def delete_handler(self, widget, **kwargs):
        for row in self.table.selection:
            self.table.data.remove(row)

    def clear_handler(self, widget, **kwargs):
        self.table.data.clear()
        # Make sure any selection is cleared.
        self.on_select_handler(self.table)

    def reset_handler(self, widget, **kwargs):
        self.table.data = self.initial_data
        # Make sure any selection is cleared.
        self.on_select_handler(self.table)

    def toggle_handler(self, widget, **kwargs):
        try:
            # Try to delete the "genre" column by accessor.
            # If the column doesn't exist, this will raise a ValueError,
            # which means we need to add it.
            self.table.remove_column("genre")
            self.btn_toggle.text = "Restore genre column"
        except ValueError:
            # Add the genre column. We provide the column *title*,
            # which is automatically converted into the data accessor `genre`.
            # If the data accessor can't be determined from the column title,
            # you could manually specify the accessor here, too.
            self.table.append_column("Genre")
            self.btn_toggle.text = "Remove genre column"

    def top_handler(self, widget, **kwargs):
        self.table.scroll_to_top()

    def bottom_handler(self, widget, **kwargs):
        self.table.scroll_to_bottom()

    def startup(self):
        self.main_window = toga.MainWindow()

        # Label to show which rows are currently selected
        self.selection_label = toga.Label(
            "Try multiple row selection.", flex=0, margin=5
        )

        # The table and its data
        self.load_data()

        self.table = toga.Table(
            columns=["Title", "Year", "Rating", "Genre"],
            data=self.initial_data,
            flex=1,
            margin=5,
            multiple_select=True,
            on_select=self.on_select_handler,
            on_activate=self.on_activate,
            missing_value="Unknown",
        )

        # Buttons
        btn_style = {"flex": 1, "margin": 3}

        self.btn_insert = toga.Button(
            "Insert random movie at top", on_press=self.insert_handler, **btn_style
        )
        self.btn_delete = toga.Button(
            "Delete selected row(s)",
            on_press=self.delete_handler,
            enabled=False,
            **btn_style,
        )
        btn_clear = toga.Button(
            "Clear table data", on_press=self.clear_handler, **btn_style
        )
        btn_reset = toga.Button(
            "Reset table data", on_press=self.reset_handler, **btn_style
        )
        self.btn_toggle = toga.Button(
            "Remove genre column", on_press=self.toggle_handler, **btn_style
        )
        btn_top = toga.Button("Scroll to top", on_press=self.top_handler, **btn_style)
        btn_bottom = toga.Button(
            "Scroll to bottom", on_press=self.bottom_handler, **btn_style
        )

        controls_1 = toga.Box(
            children=[self.btn_insert, self.btn_delete],
            direction=ROW,
        )
        controls_2 = toga.Box(
            children=[self.btn_toggle, btn_clear, btn_reset],
            direction=ROW,
        )

        controls_3 = toga.Box(
            children=[btn_top, btn_bottom],
            direction=ROW,
        )

        # Outermost box
        outer_box = toga.Box(
            children=[
                controls_1,
                controls_2,
                controls_3,
                self.table,
                self.selection_label,
            ],
            direction=COLUMN,
            margin=10,
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return TableApp("Table", "org.beeware.toga.examples.table")


if __name__ == "__main__":
    main().main_loop()
