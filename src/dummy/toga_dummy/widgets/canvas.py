from .base import Widget


class Canvas(Widget):
    def create(self):
        self._action('create Canvas')
        self.context_root = None

    def context(self):
        self._action('context')

    def set_context_root(self, context_root):
        self.context_root = context_root
        self._set_value('context root', context_root)

    def draw_callback(self, canvas, context):
        self._action('draw contexts', canvas=canvas, context=context)

    def redraw(self):
        self._action('redraw')
        for drawing_object in traverse(self.context_root):
            drawing_object(self)

    # Basic paths

    def new_path(self):
        self._action('new path')

    def closed_path(self, x, y):
        self._action('closed path', x=x, y=y)

    def move_to(self, x, y):
        self._action('move to', x=x, y=y)

    def line_to(self, x, y):
        self._action('line to', x=x, y=y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self._action('bezier curve to', cp1x=cp1x, cp1y=cp1y, cp2x=cp2x, cp2y=cp2y, x=x, y=y)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        self._action('quadratic curve to', cpx=cpx, cpy=cpy, x=x, y=y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise):
        self._action('arc', x=x, y=y, radius=radius, startangle=startangle, endangle=endangle,
                     anticlockwise=anticlockwise)

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise):
        self._action('ellipse', x=x, y=y, radiusx=radiusx, radiusy=radiusy, rotation=rotation, startangle=startangle,
                     endangle=endangle, anticlockwise=anticlockwise)

    def rect(self, x, y, width, height):
        self._action('rect', x=x, y=y, width=width, height=height)

    # Drawing Paths

    def set_color(self, color):
        self._set_value('color', color)

    def fill(self, color, fill_rule, preserve):
        self._set_value('color', color)
        self._set_value('fill rule', fill_rule)
        if preserve:
            self._action('fill preserve')
        else:
            self._action('fill')

    def stroke(self, color, line_width):
        self._set_value('color', color)
        self._set_value('line width', line_width)
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

    def write_text(self, text, x, y, font):
        self._action('write text', text=text, x=x, y=y, font=font)

    # Rehint

    def rehint(self):
        self._action('rehint Canvas')


def traverse(nested_list):
    if isinstance(nested_list, list):
        for drawing_object in nested_list:
            for subdrawing_object in traverse(drawing_object):
                yield subdrawing_object
    else:
        yield nested_list
