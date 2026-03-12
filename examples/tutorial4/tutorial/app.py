import math

import toga
from toga.colors import WHITE, rgb
from toga.constants import Baseline
from toga.fonts import SANS_SERIF


class StartApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(size=(150, 250))

        # Create empty canvas
        self.canvas = toga.Canvas(
            flex=1,
            on_resize=self.on_resize,
            on_press=self.on_press,
        )
        box = toga.Box(children=[self.canvas])

        # Add the content on the main window
        self.main_window.content = box

        # Draw tiberius on the canvas
        self.draw_tiberius()

        # Show the main window
        self.main_window.show()

    def fill_head(self):
        with self.canvas.fill(color=rgb(149, 119, 73)):
            self.canvas.move_to(112, 103)
            self.canvas.line_to(112, 113)
            self.canvas.ellipse(73, 114, 39, 47, 0, 0, math.pi)
            self.canvas.line_to(35, 84)
            self.canvas.arc(65, 84, 30, math.pi, 3 * math.pi / 2)
            self.canvas.arc(82, 84, 30, 3 * math.pi / 2, 2 * math.pi)

    def stroke_head(self):
        with self.canvas.stroke(line_width=4.0):
            with self.canvas.close_path(112, 103):
                self.canvas.line_to(112, 113)
                self.canvas.ellipse(73, 114, 39, 47, 0, 0, math.pi)
                self.canvas.line_to(35, 84)
                self.canvas.arc(65, 84, 30, math.pi, 3 * math.pi / 2)
                self.canvas.arc(82, 84, 30, 3 * math.pi / 2, 2 * math.pi)

    def draw_eyes(self):
        with self.canvas.fill(color=WHITE):
            self.canvas.arc(58, 92, 15)
            self.canvas.arc(88, 92, 15, math.pi, 3 * math.pi)

        # Draw eyes separately to avoid miter join
        with self.canvas.stroke(line_width=4.0):
            self.canvas.arc(58, 92, 15)
        with self.canvas.stroke(line_width=4.0):
            self.canvas.arc(88, 92, 15, math.pi, 3 * math.pi)

        with self.canvas.fill():
            self.canvas.arc(58, 97, 3)
            self.canvas.arc(88, 97, 3)

    def draw_horns(self):
        with self.canvas.stroke(line_width=4.0):
            with self.canvas.fill(color=rgb(212, 212, 212)):
                self.canvas.move_to(112, 99)
                self.canvas.quadratic_curve_to(145, 65, 139, 36)
                self.canvas.quadratic_curve_to(130, 60, 109, 75)

        with self.canvas.stroke(line_width=4.0):
            with self.canvas.fill(color=rgb(212, 212, 212)):
                self.canvas.move_to(35, 99)
                self.canvas.quadratic_curve_to(2, 65, 6, 36)
                self.canvas.quadratic_curve_to(17, 60, 37, 75)

    def draw_nostrils(self):
        with self.canvas.fill(color=rgb(212, 212, 212)):
            self.canvas.move_to(45, 145)
            self.canvas.bezier_curve_to(51, 123, 96, 123, 102, 145)
            self.canvas.ellipse(73, 114, 39, 47, 0, math.pi / 4, 3 * math.pi / 4)
        with self.canvas.fill():
            self.canvas.arc(63, 140, 3)
            self.canvas.arc(83, 140, 3)
        with self.canvas.stroke(line_width=4.0):
            self.canvas.move_to(45, 145)
            self.canvas.bezier_curve_to(51, 123, 96, 123, 102, 145)

    def draw_text(self):
        font = toga.Font(family=SANS_SERIF, size=20)
        self.text_width, text_height = self.canvas.measure_text("Tiberius", font)

        x = (150 - self.text_width) // 2
        y = 175

        with self.canvas.stroke(color="REBECCAPURPLE", line_width=4.0):
            self.text_border = self.canvas.rect(
                x - 5,
                y - 5,
                self.text_width + 10,
                text_height + 10,
            )
        with self.canvas.fill(color=rgb(149, 119, 73)):
            self.text = self.canvas.write_text("Tiberius", x, y, font, Baseline.TOP)

    def draw_tiberius(self):
        self.fill_head()
        self.draw_eyes()
        self.draw_horns()
        self.draw_nostrils()
        self.stroke_head()
        self.draw_text()

    def on_resize(self, widget, width, height, **kwargs):
        # On resize, center the text horizontally on the canvas. on_resize will be
        # called when the canvas is initially created, when the drawing actions won't
        # exist yet. Only attempt to reposition the text if there's a state object on
        # the canvas.
        if widget.root_state:
            left_pad = (width - self.text_width) // 2
            self.text.x = left_pad
            self.text_border.x = left_pad - 5
            widget.redraw()

    async def on_press(self, widget, x, y, **kwargs):
        await self.main_window.dialog(
            toga.InfoDialog("Hey!", f"You poked the yak at ({x}, {y})")
        )


def main():
    return StartApp("Tutorial 4", "org.beeware.toga.examples.tutorial")


if __name__ == "__main__":
    main().main_loop()
