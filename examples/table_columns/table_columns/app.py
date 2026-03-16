"""
A testing app
"""

import datetime
import locale
import random
from operator import itemgetter

from babel.dates import format_date, format_time

import toga
from toga.constants import COLUMN
from toga.sources import AccessorColumn, Column


class TitleIconColumn(Column):
    """A column that gets content from multiple attributes."""

    def value(self, row):
        return getattr(row, "title", None)

    def icon(self, row):
        return getattr(row, "icon", None)


class RatingColumn(AccessorColumn):
    """A column that displays the rating as a decimal with a red or green icon."""

    def __init__(self, heading=None, accessor=None):
        super().__init__(heading, accessor)
        self.red = toga.Icon("resources/red")
        self.green = toga.Icon("resources/green")

    def text(self, row, default=""):
        value = self.value(row)
        if value is None:
            return default
        else:
            # Format decimals according to current locale.
            return locale.format_string("%.1f", value)

    def icon(self, row):
        value = self.value(row)
        if value is None:
            return self.red
        elif value >= 7.0:
            return self.green
        else:
            return self.red


class ListStrColumn(AccessorColumn):
    """A column that displays a comma-separated list of strings."""

    def value(self, row):
        return ", ".join(str(item) for item in getattr(row, self.accessor, []))


class DateColumn(AccessorColumn):
    """A column that formats a date in a locale-appropriate way."""

    def text(self, row, default=""):
        value = self.value(row)
        if isinstance(value, datetime.date):
            return format_date(value, format="long")
        elif value is not None:
            return str(value)
        else:
            return default


class TimeColumn(AccessorColumn):
    """A column that formats a time in a locale-appropriate way."""

    def text(self, row, default=""):
        value = self.value(row)
        if isinstance(value, datetime.datetime):
            return format_time(value, format="short")
        elif value is not None:
            return str(value)
        else:
            return default


class TableColumnApp(toga.App):
    def load_data(self):
        self.bee_movies = [
            {
                "released": datetime.date(2008, 10, 17),
                "title": "The Secret Life of Bees",
                "rating": 7.3,
                "genre": ["Drama"],
                "icon": toga.Icon.DEFAULT_ICON,
            },
            {
                "released": datetime.date(2007, 10, 25),
                "title": "Bee Movie",
                "rating": 6.1,
                "genre": ["Animation", "Adventure", "Comedy"],
            },
            {
                "released": datetime.date(1978, 11, 17),
                "title": "The Bees",
                "rating": 6.3,
                "genre": ["Horror"],
            },
            {
                "released": datetime.date(2007, 2, 9),
                "title": "The Girl Who Swallowed Bees",
                "rating": 7.5,
                # No genre defined
            },
            {
                "released": datetime.date(1974, 6, 7),
                "title": "Birds Do It, Bees Do It",
                "rating": 7.3,
                "genre": ["Documentary"],
            },
            {
                "released": 1998,
                "title": "Bees: A Life for the Queen",
                "rating": 8.0,
                "genre": ["TV Movie"],
            },
            {
                "released": datetime.date(1944, 3, 20),
                "title": "Bees in Paradise",
                "rating": 5.4,
                "genre": ["Comedy", "Musical"],
            },
            {
                "released": datetime.date(1935, 7, 15),
                "title": "Keeper of the Bees",
                "rating": 6.3,
                "genre": ["Drama"],
                "icon": toga.Icon.DEFAULT_ICON,
            },
        ]
        # generate some synthetic screening information
        today = datetime.date.today()
        times = [
            datetime.datetime(today.year, today.month, today.day + 1, hour)
            for hour in [12, 16, 18, 20]
        ]
        screens = [i + 1 for i in range(len(self.bee_movies))]
        random.shuffle(screens)
        self.initial_data = sorted(
            (
                {
                    "screen": screen,
                    "time": time,
                    **movie,
                }
                for movie, screen in zip(self.bee_movies, screens, strict=True)
                for time in random.sample(times, int((movie["rating"] - 3) / 2))
            ),
            key=itemgetter("time", "screen"),
        )

    def toggle_rating(self, widget, **kwargs):
        if self.rating_column in self.table2.columns:
            self.table2.remove_column(self.rating_column)
            self.btn_rating.text = "Add Ratings"
        else:
            self.table2.append_column(self.rating_column)
            self.btn_rating.text = "Remove Ratings"

    def startup(self):
        loc = locale.setlocale(locale.LC_ALL)
        print("Using locale:", loc)

        self.main_window = toga.MainWindow()

        # The table and its data
        self.load_data()

        # Column objects can be shared
        self.rating_column = RatingColumn("Rating")

        self.table1 = toga.Table(
            columns=[
                TitleIconColumn("Title"),
                self.rating_column,
                DateColumn("Released"),
                ListStrColumn("Genre"),
            ],
            data=self.bee_movies,
            flex=1,
        )

        self.table2 = toga.Table(
            columns=[TimeColumn("Time"), "Screen", "Title"],
            data=self.initial_data,
            flex=1,
        )

        self.btn_rating = toga.Button(
            "Add Ratings", on_press=self.toggle_rating, width=150
        )
        screenings_box = toga.Box(
            children=[
                toga.Label("Screen Times", font_weight="bold", font_size=18, flex=1),
                self.btn_rating,
            ],
            align_items="center",
        )

        tablebox = toga.Box(
            children=[
                toga.Label("Movies", font_weight="bold", font_size=18, flex=1),
                self.table1,
                screenings_box,
                self.table2,
            ],
            direction=COLUMN,
            flex=1,
        )

        # Add the content on the main window
        self.main_window.content = tablebox

        # Show the main window
        self.main_window.show()


def main():
    return TableColumnApp("Table Columns", "org.beeware.toga.examples.table_columns")
