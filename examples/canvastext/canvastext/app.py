from travertino.constants import BLACK, BLUE, GREEN, RED, YELLOW, BOLD, NORMAL, ITALIC
from toga.fonts import SYSTEM, MESSAGE, SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE

import toga
from toga.style import Pack
from toga.style.pack import ROW, COLUMN

MINIMUM_FONT_SIZE = 10
MAXIMUM_FONT_SIZE = 72

STROKE = "Stroke"
FILL = "Fill"

FONTS_CHOICES = [SYSTEM, MESSAGE, SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE]


class ExampleCanvasTextApp(toga.App):
    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name, size=(750, 500))

        self.canvas = toga.Canvas(style=Pack(flex=1), on_resize=self.refresh_canvas)
        self.context_selection = toga.Selection(
            items=[STROKE, FILL], on_select=self.refresh_canvas
        )
        self.color_selection = toga.Selection(
            items=[BLACK, BLUE, GREEN, RED, YELLOW], on_select=self.refresh_canvas
        )
        self.font_selection = toga.Selection(
            items=FONTS_CHOICES, on_select=self.refresh_canvas
        )
        self.font_size_input = toga.NumberInput(
            min_value=MINIMUM_FONT_SIZE,
            max_value=MAXIMUM_FONT_SIZE,
            on_change=self.refresh_canvas
        )
        self.font_size_input.value = 20
        self.line_width_slider = toga.Slider(
            range=(1, 10), default=1, on_slide=self.refresh_canvas
        )
        self.italic_switch = toga.Switch(
            label="Italic",
            on_toggle=self.refresh_canvas
        )
        self.bold_switch = toga.Switch(
            label="Bold",
            on_toggle=self.refresh_canvas
        )
        label_style = Pack(font_size=10)
        box = toga.Box(
            style=Pack(direction=COLUMN),
            children=[
                toga.Box(
                    style=Pack(direction=ROW),
                    children=[
                        self.context_selection,
                        self.font_selection,
                        self.color_selection,
                    ],
                ),
                toga.Box(
                    style=Pack(direction=ROW),
                    children=[
                        toga.Label("Font Size:", style=label_style),
                        self.font_size_input,
                        toga.Label("Line Width:", style=label_style),
                        self.line_width_slider,
                        self.italic_switch,
                        self.bold_switch
                    ],
                ),
                self.canvas,
            ],
        )

        # Add the content on the main window
        self.main_window.content = box

        self.render_drawing(self.canvas, *self.main_window.size)

        # Show the main window
        self.main_window.show()

    def render_drawing(self, canvas, w, h):
        canvas.clear()
        with self.get_context(canvas) as context:
            self.draw_text(context, h, w)

    def draw_text(self, context, h, w):
        text = "This is a text"
        dx = w / 2
        dy = h / 2
        font = toga.Font(
            family=self.font_selection.value,
            size=self.get_font_size(),
            weight=self.get_weight(),
            style=self.get_style(),
        )
        width, height = font.measure(text, tight=True)
        context.write_text(text, dx - width / 2, dy, font)

    def get_font_size(self):
        font_size = self.font_size_input.value
        if font_size is None:
            font_size = MINIMUM_FONT_SIZE
        return font_size

    def get_weight(self):
        if self.bold_switch.is_on:
            return BOLD
        return NORMAL

    def get_style(self):
        if self.italic_switch.is_on:
            return ITALIC
        return NORMAL

    def get_context(self, canvas):
        if self.context_selection.value == STROKE:
            return canvas.stroke(
                color=str(self.color_selection.value),
                line_width=self.line_width_slider.value,
            )
        return canvas.fill(color=self.color_selection.value)

    def refresh_canvas(self, widget):
        self.render_drawing(
            self.canvas,
            self.canvas.layout.content_width,
            self.canvas.layout.content_height,
        )


def main():
    return ExampleCanvasTextApp("CanvasText", "org.beeware.widgets.canvastext")


if __name__ == "__main__":
    main().main_loop()
