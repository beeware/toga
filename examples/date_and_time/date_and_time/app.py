from datetime import date, time

import toga
from toga.constants import COLUMN, RIGHT, ROW
from toga.style import Pack


class DateAndTimeApp(toga.App):
    def changed_date(self, widget):
        print(f"{widget.id} is {widget.value.strftime('%A %d %B %Y')}")

    def changed_time(self, widget):
        print(f"{widget.id} is {widget.value.strftime('%I:%M:%S %p')}")

    def startup(self):
        self.main_window = toga.MainWindow()

        any_date_box = toga.Box(
            children=[
                toga.Label("Any date:", style=Pack(width=150, text_align=RIGHT)),
                toga.DateInput(
                    id="Any",
                    value=None,
                    on_change=self.changed_date,
                ),
            ],
            style=Pack(direction=ROW),
        )
        min_date_box = toga.Box(
            children=[
                toga.Label("With min:", style=Pack(width=150, text_align=RIGHT)),
                toga.DateInput(
                    id="Min",
                    value=None,
                    on_change=self.changed_date,
                    min="2021-01-01",
                ),
            ],
            style=Pack(direction=ROW),
        )
        max_date_box = toga.Box(
            children=[
                toga.Label("With max:", style=Pack(width=150, text_align=RIGHT)),
                toga.DateInput(
                    id="Max",
                    value=date(2021, 4, 2),
                    on_change=self.changed_date,
                    max=date(2022, 2, 1),
                ),
            ],
            style=Pack(direction=ROW),
        )
        min_max_date_box = toga.Box(
            children=[
                toga.Label(
                    "With min and max:", style=Pack(width=150, text_align=RIGHT)
                ),
                toga.DateInput(
                    id="Min-max",
                    value=date(2021, 4, 2),
                    on_change=self.changed_date,
                    min=date(2021, 1, 1),
                    max=date(2022, 2, 1),
                ),
            ],
            style=Pack(direction=ROW),
        )

        any_time_box = toga.Box(
            children=[
                toga.Label("Any time:", style=Pack(width=150, text_align=RIGHT)),
                toga.TimeInput(
                    id="Any time",
                    value=None,
                    on_change=self.changed_time,
                ),
            ],
            style=Pack(direction=ROW),
        )
        min_time_box = toga.Box(
            children=[
                toga.Label("With min:", style=Pack(width=150, text_align=RIGHT)),
                toga.TimeInput(
                    id="Min time",
                    value=None,
                    on_change=self.changed_time,
                    min="06:35:00",
                ),
            ],
            style=Pack(direction=ROW),
        )
        max_time_box = toga.Box(
            children=[
                toga.Label("With max:", style=Pack(width=150, text_align=RIGHT)),
                toga.TimeInput(
                    id="Max time",
                    value=time(10, 42),
                    on_change=self.changed_time,
                    max=time(21, 30),
                ),
            ],
            style=Pack(direction=ROW),
        )
        min_max_time_box = toga.Box(
            children=[
                toga.Label(
                    "With min and max:", style=Pack(width=150, text_align=RIGHT)
                ),
                toga.TimeInput(
                    id="Min-max time",
                    value=time(10, 42),
                    on_change=self.changed_time,
                    min=time(8, 15),
                    max=time(21, 30),
                ),
            ],
            style=Pack(direction=ROW),
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
            style=Pack(direction=COLUMN),
        )

        # Show the main window
        self.main_window.show()


def main():
    return DateAndTimeApp("Dates and Times", "org.beeware.widgets.date_and_time")


if __name__ == "__main__":
    app = main()
    app.main_loop()
