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

    def closed_path(self, x, y):
        self._action('closed path', x=x, y=y)

    def move_to(self, x, y):
        self._action('move to', x=x, y=y)

    def line_to(self, x, y):
        self._action('line to', x=x, y=y)

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self._action('bezier curve to', cp1x=cp1x, cp1y=cp1y, cp2x=cp2x, cp2y=cp2y, x=x, y=y)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        self._action('quadratic curve to', cpx=cpx, cpy=cpy, x=x, y=y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise):
        self._action('arc', x=x, y=y, radius=radius, startangle=startangle, endangle=endangle, anticlockwise=anticlockwise)

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise):
        self._action('ellipse', x=x, y=y, radiusx=radiusx, radiusy=radiusy, rotation=rotation, startangle=startangle, endangle=endangle, anticlockwise=anticlockwise)

    def rect(self, x, y, width, height):
        self._action('rect', x=x, y=y, width=width, height=height)

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
        self._action('rotate', radians=radians)

    def scale(self, sx, sy):
        self._action('scale', sx=sx, sy=sy)

    def translate(self, tx, ty):
        self._action('translate', tx=tx, ty=ty)

    def reset_transform(self):
        self._action('reset transform')

    def rehint(self):
        self._action('rehint Canvas')
