from contextlib import contextmanager
from math import pi, cos, sin, atan

import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from travertino.size import at_least

class ExampleCanvasApp(toga.App):
    def startup(self):
        # Initial width and height for the Canvas
        iwidth=600
        iheight=400

        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Setup the style selection box
        self._style_select = toga.Selection(
            items=list(self.styles), style=Pack(height=32), on_select=self.set_style
        )
        # Setup the canvas
        self._canvas = toga.Canvas(style=Pack(flex=1), on_resize=self.resize_contents)
        self._canvas.intrinsic = \
            Pack.IntrinsicSize(width=at_least(iwidth), height=at_least(iheight))

        # Add the content on the main window
        box = toga.Box(
            style=Pack(direction=COLUMN),
            children=[self._style_select, self._canvas]
        )
        self.main_window.content = box

        # Setup canvas transformation objects use to handle window moving and
        # resizing so that actual drawing code can use a fixed range of
        # coordinates
        self._canvas_translate = self._canvas.translate(iwidth/2, iheight/2)
        self._canvas_scale = self._canvas.scale(iwidth/6, iheight/6)
        self.render_drawing()

        # Show the main window
        self.main_window.show()

    def render_drawing(self):
        """Renders the dawing on the canvas by calling a set of internal
        functions that draw the various shapes
        """
        def draw_rects():
            for ctx_idx, step in enumerate(range(5, 0, -1)):
                with self.draw_context(ctx_idx) as ctx:
                    p = step/6.
                    ctx.rect(-p, -p, 2*p, 2*p)

        def draw_arcs():
            for ctx_idx, step in enumerate(range(5, 0, -1)):
                with self.draw_context(ctx_idx, 0, 0) as ctx:
                    radius = .25+step/8.
                    angle = pi*(.5+ctx_idx/8.)
                    ctx.arc(0, 0, radius, -pi, angle)

        def draw_lines():
            st_angs = [-pi/2., -pi/2., -pi/2., -pi/4., -pi/2.]
            segments = [6, 5, 4, 4, 3]
            radii = [0.9]
            for factor in [
                sin(pi/3.)/sin(8*pi/15), cos(pi/5.), cos(pi/4.), cos(pi/4)
            ]:
                radii.append(radii[-1] * factor)

            for ctx_idx, (sang, segs, r) in enumerate(zip(st_angs, segments, radii)):
                with self.draw_context(ctx_idx, r*cos(sang), r*sin(sang)) as ctx:
                    for seg in range(1, segs):
                        ang = sang + 2.*pi*seg/segs
                        ctx.line_to(r*cos(ang), r*sin(ang))

        def draw_bezier():
            for ctx_idx in range(5):
                f = (5-ctx_idx)/5.
                with self.draw_context(ctx_idx, 0.8*f, -1.) as ctx:
                    ctx.bezier_curve_to(.2*f, -.6, 1.9*f, .1, 0, 1.)
                    ctx.bezier_curve_to(-1.9*f, .1, -.2*f, -.6, -.8*f, -1.)

        def draw_ellipse():
            for ctx_idx in range(5):
                f = (5-ctx_idx)/5.
                lt, rt, tp, bm = -f, f, .9-1.8*f, .9+ctx_idx/8.
                if bm > .9:
                    ang = atan((bm-.9)/(bm-tp))
                else:
                    ang = 0
                with self.draw_context(ctx_idx, 0, .9) as ctx:
                    ctx.ellipse(0, bm, rt, bm-tp, 0.,ang-pi, -ang)

        def draw_quadratic():
            for ctx_idx in range(5):
                f = 0.9*(5-ctx_idx)/5.
                with self.draw_context(ctx_idx, -.9, -f) as ctx:
                    ctx.quadratic_curve_to(.7+f, 0., -.9, f)

        draw_funcs = [
            draw_rects, draw_arcs, draw_lines, draw_bezier, draw_ellipse,
            draw_quadratic
        ]
        # Each draw function draws in coordinates ranging from -1 to 1, so
        # we use translations to make the different drawings appear side by
        # side in a (-3..3, -2..2) grid.
        xmoves = [-2, 2, 2, -4, 2, 2]
        ymoves = [-1, 0, 0, 2, 0, 0]

        for df, tx, ty in zip(draw_funcs, xmoves, ymoves):
            self._canvas.translate(tx, ty)
            df()

    def draw_context(self, ctx_idx, stx=None, sty=None):
        """Setup a drawing context that defines the line stroking and filling
        style according to user selection in the style box

        This function returns a context manager that is meant to be used for
        calling the various drawing functions.
        """
        strokes=[
            {'line_width': 0.025, 'line_dash': (0.01, 0.05)},
            {'line_width': 0.025, 'line_dash': (0.1,)},
            {'line_width': 0.025, 'line_dash': None},
            {'line_width': 0.05, 'line_dash': None},
            {'line_width': 0.1, 'line_dash': None},
        ]
        stroke = strokes[ctx_idx]
        colors = ['red', 'yellow', 'green', 'aqua', 'blue']
        color = colors[ctx_idx]

        style = self.styles[self._style_select.value]
        return style(self, stroke, color, stx, sty)

    @contextmanager
    def _style_open_lines(self, stroke, color, stx, sty):
        with self._canvas.stroke(**stroke) as ctx:
            if stx is not None and sty is not None:
                ctx.move_to(stx, sty)
            yield ctx

    @contextmanager
    def _style_closed_lines(self, stroke, color, stx, sty):
        with self._canvas.stroke(**stroke) as ctx:
            if stx is not None and sty is not None:
                with ctx.closed_path(stx, sty) as ctx_c:
                    yield ctx_c
            else:
                yield ctx

    @contextmanager
    def _style_filled(self, stroke, color, stx, sty):
        with self._canvas.fill(color=color) as ctx:
            if stx is not None and sty is not None:
                ctx.move_to(stx, sty)
            yield ctx

    @contextmanager
    def _style_stroked_filled(self, stroke, color, stx, sty):
        with self._canvas.stroke(**stroke) as stroke:
            with stroke.fill(color=color, preserve=True) as ctx:
                if stx is not None and sty is not None:
                    with ctx.closed_path(stx, sty) as ctx_c:
                        yield ctx_c
                else:
                    yield ctx

    # Define the set of styles selectable the user, the keys are the user
    # selectable string, the values are functions that implement the selected
    # styles by returning drawing context objects
    styles = {
        'Fill, Close & Stroke': _style_stroked_filled,
        'Stroke': _style_open_lines,
        'Close & Stroke': _style_closed_lines,
        'Fill only': _style_filled,
    }

    def set_style(self, widget):
        """Called when the user selects a style from the styles selection box
        """
        self.clear()
        self.render_drawing()
        self._canvas.redraw()

    def clear(self):
        """Used to clear the canvas
        """
        self._canvas.clear()
        # Once we cleared the canvas, restore the translation and scale objects
        # so the canvas contents keeps matching the window size and position
        self._canvas.add_draw_obj(self._canvas_translate)
        self._canvas.add_draw_obj(self._canvas_scale)

    def resize_contents(self, canvas):
        """Called when the window (and therefore the Canvas) is resized

        Adjusts the Canvas scale and translation objects to make the Canvas
        contents fill the available space while maintaining aspect ratio
        """
        factor = min(
            canvas.layout.content_width/6,
            canvas.layout.content_height/4,
        )
        self._canvas_scale.sx = factor
        self._canvas_scale.sy = factor
        self._canvas_translate.tx = canvas.layout.content_width/2
        self._canvas_translate.ty = canvas.layout.content_height/2

def main():
    return ExampleCanvasApp('Canvas More', 'org.beeware.widgets.canvas')


if __name__ == '__main__':
    main().main_loop()
