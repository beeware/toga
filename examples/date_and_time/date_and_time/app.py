from datetime import date, time

import toga
from toga.constants import COLUMN, RIGHT, ROW


class DateAndTimeApp(toga.App):
    def changed_date(self, widget):
        print(f"{widget.id} is {widget.value.strftime('%A %d %B %Y')}")

    def changed_time(self, widget):
        print(f"{widget.id} is {widget.value.strftime('%I:%M:%S %p')}")

    def startup(self):
        self.main_window = toga.MainWindow()

        any_date_box = toga.Box(
            children=[
                toga.Label("Any date:", width=150, text_align=RIGHT),
                toga.DateInput(
                    id="Any",
                    value=None,
                    on_change=self.changed_date,
                ),
            ],
            direction=ROW,
        )
        min_date_box = toga.Box(
            children=[
                toga.Label("With min:", width=150, text_align=RIGHT),
                toga.DateInput(
                    id="Min",
                    value=None,
                    on_change=self.changed_date,
                    min="2021-01-01",
                ),
            ],
            direction=ROW,
        )
        max_date_box = toga.Box(
            children=[
                toga.Label("With max:", width=150, text_align=RIGHT),
                toga.DateInput(
                    id="Max",
                    value=date(2021, 4, 2),
                    on_change=self.changed_date,
                    max=date(2022, 2, 1),
                ),
            ],
            direction=ROW,
        )
        min_max_date_box = toga.Box(
            children=[
                toga.Label("With min and max:", width=150, text_align=RIGHT),
                toga.DateInput(
                    id="Min-max",
                    value=date(2021, 4, 2),
                    on_change=self.changed_date,
                    min=date(2021, 1, 1),
                    max=date(2022, 2, 1),
                ),
            ],
            direction=ROW,
        )

        any_time_box = toga.Box(
            children=[
                toga.Label("Any time:", width=150, text_align=RIGHT),
                toga.TimeInput(
                    id="Any time",
                    value=None,
                    on_change=self.changed_time,
                ),
            ],
            direction=ROW,
        )
        min_time_box = toga.Box(
            children=[
                toga.Label("With min:", width=150, text_align=RIGHT),
                toga.TimeInput(
                    id="Min time",
                    value=None,
                    on_change=self.changed_time,
                    min="06:35:00",
                ),
            ],
            direction=ROW,
        )
        max_time_box = toga.Box(
            children=[
                toga.Label("With max:", width=150, text_align=RIGHT),
                toga.TimeInput(
                    id="Max time",
                    value=time(10, 42),
                    on_change=self.changed_time,
                    max=time(21, 30),
                ),
            ],
            direction=ROW,
        )
        min_max_time_box = toga.Box(
            children=[
                toga.Label("With min and max:", width=150, text_align=RIGHT),
                toga.TimeInput(
                    id="Min-max time",
                    value=time(10, 42),
                    on_change=self.changed_time,
                    min=time(8, 15),
                    max=time(21, 30),
                ),
            ],
            direction=ROW,
        )

        self.main_window.content = toga.Box(
            children=[
                any_date_box,
                min_date_box,
                max_date_box,
                min_max_date_box,
                any_time_box,
                min_time_box,
                max_time_box,
                min_max_time_box,
            ],
            direction=COLUMN,
        )

        # Show the main window
        self.main_window.show()


def main():
    return DateAndTimeApp("Dates and Times", "org.beeware.toga.examples.date_and_time")


if __name__ == "__main__":
    main().main_loop()
