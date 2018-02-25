import re

from .base import Widget


class Canvas(Widget):
    def create(self):
        self._action('create Canvas')

    def set_context(self, context, remove=False):
        self._set_value('context', context, remove)

    def line_width(self, width=2.0, remove=False):
        self._set_value('line_width', width, remove)

    def fill_style(self, color=None, remove=False):
        if color is not None:
            num = re.search('^rgba\((\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*)\)$', color)
            if num is not None:
                r = num.group(1)
                g = num.group(2)
                b = num.group(3)
                a = num.group(4)
                rgba = str(r + ', ' + g + ', ' + b + ', ' + a)
                self._set_value('fill_style', rgba, remove)
            else:
                pass
                # Support future colosseum versions
                # for named_color, rgb in colors.NAMED_COLOR.items():
                #     if named_color == color:
                #         exec('self._set_value('fill_style', color)
        else:
            # set color to black
            self._set_value('fill_style', '0, 0, 0, 1', remove)

    def stroke_style(self, color=None, remove=False):
        self.fill_style(color, remove)

    def close_path(self, remove=False):
        self._action('close path', remove=remove)

    def closed_path(self, x, y, remove=False):
        self._action('closed path', x=x, y=y, remove=remove)

    def move_to(self, x, y, remove=False):
        self._action('move to', x=x, y=y, remove=remove)

    def line_to(self, x, y, remove=False):
        self._action('line to', x=x, y=y, remove=remove)

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, remove=False):
        self._action('bezier curve to', cp1x=cp1x, cp1y=cp1y, cp2x=cp2x, cp2y=cp2y, x=x, y=y, remove=remove)

    def quadratic_curve_to(self, cpx, cpy, x, y, remove=False):
        self._action('quadratic curve to', cpx=cpx, cpy=cpy, x=x, y=y, remove=remove)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise, remove=False):
        self._action('arc', x=x, y=y, radius=radius, startangle=startangle, endangle=endangle,
                     anticlockwise=anticlockwise, remove=remove)

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise, remove=False):
        self._action('ellipse', x=x, y=y, radiusx=radiusx, radiusy=radiusy, rotation=rotation, startangle=startangle,
                     endangle=endangle, anticlockwise=anticlockwise, remove=remove)

    def rect(self, x, y, width, height, remove=False):
        self._action('rect', x=x, y=y, width=width, height=height, remove=remove)

    # Drawing Paths

    def fill(self, fill_rule, preserve, remove=False):
        self._set_value('fill rule', fill_rule, remove)
        if preserve:
            self._action('fill preserve', remove=remove)
        else:
            self._action('fill', remove=remove)

    def stroke(self, remove=False):
        self._action('stroke', remove=remove)

    # Transformations

    def rotate(self, radians, remove=False):
        self._action('rotate', radians=radians, remove=remove)

    def scale(self, sx, sy, remove=False):
        self._action('scale', sx=sx, sy=sy, remove=remove)

    def translate(self, tx, ty, remove=False):
        self._action('translate', tx=tx, ty=ty, remove=remove)

    def reset_transform(self, remove=False):
        self._action('reset transform')

    def write_text(self, text, x, y, font, remove=False):
        self._action('write text', text=text, x=x, y=y, font=font, remove=remove)

    def rehint(self):
        self._action('rehint Canvas')
