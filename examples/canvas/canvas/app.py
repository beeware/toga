import math

from travertino.constants import BLACK, BLUE, GREEN, RED, YELLOW, BOLD, NORMAL, ITALIC
from toga.fonts import SYSTEM, MESSAGE, SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE

import toga
from toga.style import Pack
from toga.style.pack import ROW, COLUMN
from toga.widgets.canvas import FillRule

STROKE = "Stroke"
FILL = "Fill"

INSTRUCTIONS = "instructions"
TRIANGLE = "triangle"
TRIANGLES = "triangles"
RECTANGLE = "rectangle"
ELLIPSE = "ellipse"
HALF_ELLIPSE = "half ellipse"
ICE_CREAM = "ice cream"
SMILE = "smile"
SEA = "sea"
STAR = "star"

CONTINUOUS = "continuous"
DASH_1_1 = "dash 1-1"
DASH_1_2 = "dash 1-2"
DASH_2_3_1 = "dash 2-3-1"


class ExampleCanvasApp(toga.App):

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name, size=(750, 500))

        self.canvas = toga.Canvas(
            style=Pack(flex=1),
            on_resize=self.refresh_canvas,
            on_press=self.on_press,
            on_drag=self.on_drag,
            on_release=self.on_release
        )
        self.context_selection = toga.Selection(items=[STROKE, FILL], on_select=self.refresh_canvas)
        self.drawing_shape_instructions = {
            INSTRUCTIONS: self.draw_instructions,
            TRIANGLE: self.draw_triangle,
            TRIANGLES: self.draw_triangles,
            RECTANGLE: self.draw_rectangle,
            ELLIPSE: self.draw_ellipse,
            HALF_ELLIPSE: self.draw_half_ellipse,
            ICE_CREAM: self.draw_ice_cream,
            SMILE: self.draw_smile,
            SEA: self.draw_sea,
            STAR: self.draw_star,
        }
        self.dash_patterns = {
            CONTINUOUS: None,
            DASH_1_1: [1, 1],
            DASH_1_2: [1, 2],
            DASH_2_3_1: [2, 3, 1]
        }
        self.shape_selection = toga.Selection(
            items=list(self.drawing_shape_instructions.keys()),
            on_select=self.on_shape_change
        )
        self.color_selection = toga.Selection(
            items=[BLACK, BLUE, GREEN, RED, YELLOW],
            on_select=self.refresh_canvas
        )
        self.fill_rule_selection = toga.Selection(
            items=[value.name.lower() for value in FillRule],
            on_select=self.refresh_canvas
        )
        self.line_width_slider = toga.Slider(
            range=(1, 10),
            default=1,
            on_slide=self.refresh_canvas
        )
        self.dash_pattern_selection = toga.Selection(
            items=list(self.dash_patterns.keys()),
            on_select=self.refresh_canvas
        )
        self.clicked_point = None
        self.translation = None
        self.scale_x_slider = toga.Slider(
            range=(0, 2),
            default=1,
            tick_count=10,
            on_slide=self.refresh_canvas
        )
        self.scale_y_slider = toga.Slider(
            range=(0, 2),
            default=1,
            tick_count=10,
            on_slide=self.refresh_canvas
        )
        self.rotation_slider = toga.Slider(
            range=(-math.pi, math.pi),
            default=0,
            on_slide=self.refresh_canvas
        )
        self.font_selection = toga.Selection(
            items=[
                SYSTEM,
                MESSAGE,
                SERIF,
                SANS_SERIF,
                CURSIVE,
                FANTASY,
                MONOSPACE
            ],
            on_select=self.refresh_canvas
        )
        self.font_size = toga.NumberInput(
            min_value=10,
            max_value=72,
            default=20,
            on_change=self.refresh_canvas
        )
        self.italic_switch = toga.Switch(
            label="italic",
            on_toggle=self.refresh_canvas
        )
        self.bold_switch = toga.Switch(
            label="bold",
            on_toggle=self.refresh_canvas
        )
        label_style = Pack(font_size=10, padding_left=5)

        # Add the content on the main window
        box = toga.Box(
            style=Pack(direction=COLUMN),
            children=[
                toga.Box(
                    style=Pack(direction=ROW, padding=5),
                    children=[
                        self.context_selection,
                        self.shape_selection,
                        self.color_selection,
                        self.fill_rule_selection
                    ]
                ),
                toga.Box(
                    style=Pack(direction=ROW, padding=5),
                    children=[
                        toga.Label("Line Width:", style=label_style),
                        self.line_width_slider,
                        self.dash_pattern_selection
                    ]
                ),
                toga.Box(
                    style=Pack(direction=ROW, padding=5),
                    children=[
                        toga.Label("Rotation:", style=label_style),
                        self.rotation_slider,
                        toga.Label("X Scale:", style=label_style),
                        self.scale_x_slider,
                        toga.Label("Y Scale:", style=label_style),
                        self.scale_y_slider,
                        toga.Button(
                            label="Reset transform",
                            on_press=self.reset_transform
                        )
                    ]
                ),
                toga.Box(
                    style=Pack(direction=ROW, padding=5),
                    children=[
                        toga.Label("Font Family:", style=label_style),
                        self.font_selection,
                        toga.Label("Font Size:", style=label_style),
                        self.font_size,
                        self.bold_switch,
                        self.italic_switch
                    ]
                ),
                self.canvas
            ]
        )
        self.main_window.content = box

        self.change_shape()
        self.render_drawing()

        # Show the main window
        self.main_window.show()

    @property
    def height(self):
        return self.canvas.layout.content_height

    @property
    def width(self):
        return self.canvas.layout.content_width

    @property
    def translation(self):
        return self._x_translation, self._y_translation

    @translation.setter
    def translation(self, xy_tuple):
        if xy_tuple is None:
            self.x_translation = self.y_translation = 0
        else:
            self.x_translation, self.y_translation = xy_tuple

    @property
    def x_translation(self):
        return self._x_translation

    @x_translation.setter
    def x_translation(self, x_translation):
        self._x_translation = x_translation

    @property
    def y_translation(self):
        return self._y_translation

    @y_translation.setter
    def y_translation(self, y_translation):
        self._y_translation = y_translation

    def reset_transform(self, widget):
        self.translation = None
        self.scale_x_slider.value = 1
        self.scale_y_slider.value = 1
        self.rotation_slider.value = 0
        self.refresh_canvas(widget)

    def on_shape_change(self, widget):
        self.change_shape()
        self.refresh_canvas(widget)

    def on_press(self, widget, x, y, clicks):
        self.clicked_point = (x, y)
        self.render_drawing()

    def on_drag(self, widget, x, y, clicks):
        tx = self.x_translation + x - self.clicked_point[0]
        ty = self.y_translation + y - self.clicked_point[1]
        self.translation = (tx, ty)
        self.clicked_point = (x, y)
        self.render_drawing()

    def on_release(self, widget, x, y, clicks):
        if clicks >= 2:
            self.x_translation = x - self.width / 2
            self.y_translation = y - self.height / 2
        self.clicked_point = None
        self.render_drawing()

    def change_shape(self):
        is_text = self.shape_selection.value == INSTRUCTIONS
        self.font_selection.enabled = is_text
        self.font_size.enabled = is_text
        self.italic_switch.enabled = is_text
        self.bold_switch.enabled = is_text

    def refresh_canvas(self, widget):
        self.render_drawing()

    def render_drawing(self):
        self.canvas.clear()
        self.canvas.translate(
            self.width / 2 + self.x_translation, self.height / 2 + self.y_translation
        )
        self.canvas.rotate(self.rotation_slider.value)
        self.canvas.scale(self.scale_x_slider.value, self.scale_y_slider.value)
        self.canvas.translate(-self.width / 2, -self.height / 2)
        with self.get_context(self.canvas) as context:
            self.draw_shape(context)
        self.canvas.reset_transform()

    def draw_shape(self, context):
        # Scale to the smallest axis to maintain aspect ratio
        factor = min(self.width, self.height)
        drawing_instructions = self.drawing_shape_instructions.get(
            self.shape_selection.value, None
        )
        if drawing_instructions is not None:
            drawing_instructions(context, factor)

    def draw_triangle(self, context, factor):
        # calculate offsets to centralize drawing in the bigger axis
        dx = (self.width - factor) / 2
        dy = (self.height - factor) / 2
        with context.closed_path(dx + factor / 3, dy + factor / 3) as closer:
            closer.line_to(dx + 2 * factor / 3, dy + 2 * factor / 3)
            closer.line_to(dx + 2 * factor / 3, dy + factor / 3)

    def draw_triangles(self, context, factor):
        # calculate offsets to centralize drawing in the bigger axis
        dx = self.width / 2
        dy = self.height / 2
        triangle_size = factor / 5
        gap = factor / 12
        context.move_to(dx - 2 * triangle_size - gap, dy - 2 * triangle_size)
        context.line_to(dx - gap, dy - 2 * triangle_size)
        context.line_to(dx - triangle_size - gap, dy - triangle_size)
        context.line_to(dx - 2 * triangle_size - gap, dy - 2 * triangle_size)
        context.move_to(dx + gap, dy - 2 * triangle_size)
        context.line_to(dx + 2 * triangle_size + gap, dy - 2 * triangle_size)
        context.line_to(dx + triangle_size + gap, dy - triangle_size)
        context.line_to(dx + gap, dy - 2 * triangle_size)
        context.move_to(dx - triangle_size, dy - triangle_size + gap)
        context.line_to(dx + triangle_size, dy - triangle_size + gap)
        context.line_to(dx, dy + gap)
        context.line_to(dx - triangle_size, dy - triangle_size + gap)

    def draw_rectangle(self, context, factor):
        dx = self.width / 2
        dy = self.height / 2
        context.rect(dx - factor / 3, dy - factor / 6, 2 * factor / 3, factor / 3)

    def draw_ellipse(self, context, factor):
        rx = factor / 3
        ry = factor / 4

        context.ellipse(self.width / 2, self.height / 2, rx, ry)

    def draw_half_ellipse(self, context, factor):
        x_center = self.width / 2
        y_center = self.height / 2
        rx = factor / 3
        ry = factor / 4

        with context.closed_path(x_center + rx, y_center) as closer:
            closer.ellipse(x_center, y_center, rx, ry, 0, 0, math.pi)

    def draw_ice_cream(self, context, factor):
        dx = self.width / 2
        dy = self.height / 2 - factor / 6
        with context.closed_path(dx - factor / 5, dy) as closer:
            closer.arc(dx, dy, factor / 5, math.pi, 2 * math.pi)
            closer.line_to(dx, dy + 2 * factor / 5)

    def draw_smile(self, context, factor):
        dx = self.width / 2
        dy = self.height / 2 - factor / 5
        with context.closed_path(dx - factor / 5, dy) as closer:
            closer.quadratic_curve_to(dx, dy + 3 * factor / 5, dx + factor / 5, dy)
            closer.quadratic_curve_to(dx, dy + factor / 5, dx - factor / 5, dy)

    def draw_sea(self, context, factor):
        dx = self.width / 2
        dy = self.height / 2
        with context.closed_path(dx - 1 * factor / 5, dy - 1 * factor / 5) as closer:
            closer.bezier_curve_to(
                dx - 1 * factor / 10,
                dy,
                dx + 1 * factor / 10,
                dy - 2 * factor / 5,
                dx + 1 * factor / 5,
                dy - 1 * factor / 5)
            closer.line_to(dx + 1 * factor / 5, dy + 1 * factor / 5)
            closer.line_to(dx - 1 * factor / 5, dy + 1 * factor / 5)

    def draw_star(self, context, factor):
        sides = 5
        dx = self.width / 2
        dy = self.height / 2
        radius = factor / 5
        rotation_angle = 4 * math.pi / sides
        with context.closed_path(dx, dy - radius) as closer:
            for i in range(1, sides):
                closer.line_to(dx + radius * math.sin(i * rotation_angle),
                               dy - radius * math.cos(i * rotation_angle))

    def draw_instructions(self, context, factor):
        text = """To control this example:
1. Use the above settings.
2. Press once and drag to translate the image.
3. Press twice on a location to center the image on it.
"""
        dx = self.width / 2
        dy = self.height / 2
        font = toga.Font(
            family=self.font_selection.value,
            size=self.font_size.value,
            weight=self.get_weight(),
            style=self.get_style(),
        )
        width, height = self.canvas.measure_text(text, font, tight=True)
        context.write_text(text, dx - width / 2, dy, font)

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
                line_dash=self.dash_patterns[self.dash_pattern_selection.value]
            )
        return canvas.fill(
            color=self.color_selection.value,
            fill_rule=self.fill_rule_selection.value
        )


def main():
    return ExampleCanvasApp('Canvas', 'org.beeware.widgets.canvas')


if __name__ == '__main__':
    main().main_loop()
