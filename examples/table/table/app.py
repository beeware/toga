import random

import toga
from toga.constants import COLUMN, ROW

headings = ["Title", "Year", "Rating", "Genre"]


class TableApp(toga.App):
    lbl_fontsize = None

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

    # Table callback functions
    def on_select_handler1(self, widget, **kwargs):
        row = self.table1.selection
        self.label_table1.text = (
            f"You selected row: {row.title[1]}"
            if row is not None
            else "No row selected"
        )

    def on_select_handler2(self, widget, **kwargs):
        if self.table2.selection is not None:
            self.label_table2.text = f"Rows selected: {len(self.table2.selection)}"
        else:
            self.label_table2.text = "No row selected"

    async def on_activate1(self, widget, row, **kwargs):
        await self.main_window.dialog(
            toga.InfoDialog(
                title="movie selection",
                message=self.build_activate_message(row=row, table_index=1),
            )
        )

    async def on_activate2(self, widget, row, **kwargs):
        await self.main_window.dialog(
            toga.InfoDialog(
                title="movie selection",
                message=self.build_activate_message(row=row, table_index=2),
            )
        )

    # Button callback functions
    def insert_handler(self, widget, **kwargs):
        self.table1.data.insert(0, random.choice(self.bee_movies))

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
        self.table1.data = self.bee_movies

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

    def top_handler(self, widget, **kwargs):
        self.table1.scroll_to_top()

    def bottom_handler(self, widget, **kwargs):
        self.table1.scroll_to_bottom()

    def startup(self):
        self.main_window = toga.MainWindow()

        # Label to show which row is currently selected.
        self.label_table1 = toga.Label("Ready.", flex=1, margin_right=5)
        self.label_table2 = toga.Label(
            "Try multiple row selection.", flex=1, margin_left=5
        )
        labelbox = toga.Box(
            children=[self.label_table1, self.label_table2],
            flex=0,
            margin_top=5,
        )

        # Change font size
        lbl_fontlabel = toga.Label("Font size =")
        self.lbl_fontsize = toga.Label("10")
        btn_reduce_size = toga.Button(" - ", on_press=self.reduce_fontsize, width=40)
        btn_increase_size = toga.Button(
            " + ", on_press=self.increase_fontsize, width=40
        )
        font_box = toga.Box(
            children=[
                toga.Box(
                    children=[btn_reduce_size, btn_increase_size],
                    direction=ROW,
                ),
                toga.Box(
                    children=[lbl_fontlabel, self.lbl_fontsize],
                    direction=ROW,
                ),
            ],
            direction=COLUMN,
        )

        # Data to populate the table.
        self.load_data()
        if toga.platform.current_platform == "android":
            # FIXME: beeware/toga#1392 - Android Table doesn't allow lots of content
            table_data = self.bee_movies * 10
        else:
            table_data = self.bee_movies * 1000

        self.table1 = toga.Table(
            headings=headings,
            data=table_data,
            flex=1,
            margin_right=5,
            font_family="monospace",
            font_size=int(self.lbl_fontsize.text),
            font_style="italic",
            multiple_select=False,
            on_select=self.on_select_handler1,
            on_activate=self.on_activate1,
            missing_value="Unknown",
        )

        self.table2 = toga.Table(
            headings=None,
            accessors=[h.lower() for h in headings],
            data=self.table1.data,
            multiple_select=True,
            flex=1,
            margin_left=5,
            on_select=self.on_select_handler2,
            on_activate=self.on_activate2,
            missing_value="?",
        )

        tablebox = toga.Box(children=[self.table1, self.table2], flex=1)

        # Buttons
        btn_insert = toga.Button("Insert", on_press=self.insert_handler, flex=1)
        btn_delete = toga.Button("Delete", on_press=self.delete_handler, flex=1)
        btn_clear = toga.Button("Clear", on_press=self.clear_handler, flex=1)
        btn_reset = toga.Button("Reset", on_press=self.reset_handler, flex=1)
        btn_toggle = toga.Button("Column", on_press=self.toggle_handler, flex=1)
        btn_top = toga.Button("Top", on_press=self.top_handler, flex=1)
        btn_bottom = toga.Button("Bottom", on_press=self.bottom_handler, flex=1)

        controls_1 = toga.Box(
            children=[font_box, btn_insert, btn_delete, btn_clear],
            direction=ROW,
            margin_bottom=5,
        )
        controls_2 = toga.Box(
            children=[btn_reset, btn_toggle, btn_top, btn_bottom],
            direction=ROW,
            margin_bottom=5,
        )

        # Most outer box
        outer_box = toga.Box(
            children=[controls_1, controls_2, tablebox, labelbox],
            flex=1,
            direction=COLUMN,
            margin=10,
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()

    def reduce_fontsize(self, widget):
        font_size = int(self.lbl_fontsize.text) - 1
        self.lbl_fontsize.text = str(font_size)
        font = toga.Font(family="monospace", size=font_size, style="italic")
        self.table1._impl.set_font(font)

    def increase_fontsize(self, widget):
        font_size = int(self.lbl_fontsize.text) + 1
        self.lbl_fontsize.text = str(font_size)
        font = toga.Font(family="monospace", size=font_size, style="italic")
        self.table1._impl.set_font(font)

    @classmethod
    def build_activate_message(cls, row, table_index):
        adjective = random.choice(
            ["magnificent", "amazing", "awesome", "life-changing"]
        )
        genre = (getattr(row, "genre", "") or "no-genre").lower()
        return (
            f"You selected the {adjective} {genre} movie "
            f"{row.title[1]} ({row.year}) from Table {table_index}"
        )


def main():
    return TableApp("Table", "org.beeware.toga.examples.table")


if __name__ == "__main__":
    main().main_loop()
