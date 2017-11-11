import re
from .base import Widget


class Canvas(Widget):
    def create(self):
        self._action('create Canvas')

    def set_on_draw(self, handler):
        self._set_value('on_draw', handler)

    def set_context(self, context):
        self._set_value('context', context)

    def line_width(self, width=2.0):
        self._set_value('line_width', width)

    def fill_style(self, color=None):
        if color is not None:
            num = re.search('^rgba\((\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*)\)$', color)
            if num is not None:
                r = num.group(1)
                g = num.group(2)
                b = num.group(3)
                a = num.group(4)
                rgba = str(r + ', ' + g + ', ' + b + ', ' + a)
                self._set_value('fill_style', rgba)
            else:
                pass
                # Support future colosseum versions
                # for named_color, rgb in colors.NAMED_COLOR.items():
                #     if named_color == color:
                #         exec('self._set_value('fill_style', color)
        else:
            # set color to black
            self._set_value('fill_style', '0, 0, 0, 1')

    def stroke_style(self, color=None):
        self.fill_style(color)

    def close_path(self):
        self._action('close path')

    def move_to(self, x, y):
        self._action('move to (' + x + ' ,' + y + ')')

    def line_to(self, x, y):
        self._action('line to (' + x + ' ,' + y + ')')

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self._action('bezier curve to ' + cp1x + ' ,' + cp1y + ' ,' + cp2x + ' ,' + cp2y + ' ,' + x + ' ,' + y)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        self._action('quadratic curve to (' + cpx + ' ,' + cpy + ' ,' + x + ' ,' + y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise):
        self._action(
            'arc (' + x + ' ,' + y + ' ,' + radius + ' ,' + startangle + ' ,' + endangle + ' ,' + anticlockwise)

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise):
        self._action(
            'ellipse (' + x + ' ,' + y + ' ,' + radiusx + ' ,' + radiusy + ' ,' + rotation + ' ,' + startangle + ' ,' + endangle + ' ,' + anticlockwise)

    def rect(self, x, y, width, height):
        self._action('rect (' + x + ' ,' + y + ' ,' + width + ' ,' + height)

    # Drawing Paths

    def fill(self, fill_rule, preserve):
        self._set_value('fill rule', fill_rule)
        if preserve:
            self._action('fill preserve')
        else:
            self._action('fill')

    def stroke(self):
        self._action('stroke')

    # Transformations

    def rotate(self, radians):
        self._action('rotate ' + radians)

    def scale(self, sx, sy):
        self._action('scale ' + sx + ' ' + sy)

    def translate(self, tx, ty):
        self._action('translate ' + tx + ' ' + ty)

    def reset_transform(self):
        self._action('reset transform')

    def rehint(self):
        self._action('rehint Canvas')
