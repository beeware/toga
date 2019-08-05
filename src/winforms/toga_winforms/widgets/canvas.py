from .base import Widget
from travertino.size import at_least
from toga_winforms.libs import WinForms, Pen, Color, SolidBrush, Brush, Bitmap, WinFont, Point
from toga_winforms.colors import native_color
import math


# function to turn radians into degrees
def get_degrees(radians):
    return int(radians * (180 / math.pi))


class Canvas(Widget):

    # Create the WinForms object to draw on. going to use a panel for this
    def create(self):
        self.native = WinForms.PictureBox()
        self.native.Dock = WinForms.DockStyle.Fill
        self.pen = Pen(Color.Black)
        self.bmp = Bitmap(1000, 1000)
        self.brush = None
        self.curX = 0
        self.curY = 0

    # Will set each object in the object list to be drawn

    def redraw(self):
        bit = Bitmap(1000, 1000)
        bitgraphics = self.native.CreateGraphics().FromImage(bit)
        bitgraphics.DrawImage(self.bmp, 0, 0, self.bmp.Width, self.bmp.Height)
        bitgraphics.Dispose()

        self.bmp = bit

        self.interface.drawing_objects[-1]._draw(self.interface._impl)

        self.native.Image = self.bmp

    # Basic paths

    def new_path(self, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.new_path()')

    def closed_path(self, x, y, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.closed_path()')

    def move_to(self, x, y, *args, **kwargs):
        self.curX = x
        self.curY = y

    def line_to(self, x, y, *args, **kwargs):
        graphics = self.native.CreateGraphics().FromImage(self.bmp)
        graphics.DrawLine(self.pen, self.curX, self.curY, x, y)
        graphics.Dispose()

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, *args, **kwargs):
        graphics = self.native.CreateGraphics().FromImage(self.bmp)
        graphics.DrawBezier(self.pen, float(self.curX), float(self.curY), float(cp1x), float(cp1y), 
            float(cp2x), float(cp2y), float(x), float(y))
        graphics.Dispose()

    def quadratic_curve_to(self, cpx, cpy, x, y, *args, **kwargs):
        points = []
        points.append(Point(self.curX, self.curY))
        points.append(Point(cpx, cpy))
        points.append(Point(x, y))

        graphics = self.native.CreateGraphics().FromImage(self.bmp)
        graphics.DrawCurve(self.pen, points)
        graphics.Dispose()

    def arc(self, x, y, radius, startangle, endangle, anticlockwise, *args, **kwargs):
        if self.brush is not None:
            graphics = self.native.CreateGraphics().FromImage(self.bmp)
            graphics.FillPie(self.brush, x, y, radius, radius, get_degrees(startangle), get_degrees(endangle))
            graphics.Dispose()
        else:
            graphics = self.native.CreateGraphics().FromImage(self.bmp)
            print(get_degrees(startangle))
            graphics.DrawArc(self.pen, x, y, radius, radius, get_degrees(startangle), get_degrees(endangle))
            graphics.Dispose()

    def ellipse(
        self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise, *args, **kwargs
    ):
        if self.brush is not None:
            graphics = self.native.CreateGraphics().FromImage(self.bmp)
            graphics.FillEllipse(self.brush, x, y, radiusx, radiusy)
            graphics.Dispose()
        else:
            graphics = self.native.CreateGraphics().FromImage(self.bmp)
            graphics.DrawEllipse(self.pen, x, y, radiusx, radiusy)
            graphics.Dispose()

    def rect(self, x, y, width, height, *args, **kwargs):
        if self.brush is not None:
            graphics = self.native.CreateGraphics().FromImage(self.bmp)
            graphics.FillRectangle(self.brush, x, y, width, height)
            graphics.Dispose()
        else:
            graphics = self.native.CreateGraphics().FromImage(self.bmp)
            graphics.DrawRectangle(self.pen, x, y, width, height)
            graphics.Dispose()

    # Drawing Paths

    def fill(self, color, fill_rule, preserve, *args, **kwargs):
        if color is None:
            self.brush = None
        else:
            self.brush = SolidBrush(native_color(color))

    def stroke(self, color, line_width, line_dash, *args, **kwargs):
        self.pen.Color = native_color(color)
        self.pen.Width = line_width

    # Transformations

    def rotate(self, radians, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.rotate()')

    def scale(self, sx, sy, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.scale()')

    def translate(self, tx, ty, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.translate()')

    def reset_transform(self, *args, **kwargs):
        self.interface.factory.not_implemented('Canvas.reset_transform()')

    # Text

    def write_text(self, text, x, y, font, *args, **kwargs):
        win_font = WinFont(str(font.family), float(font.size))
        if self.brush is not None:
            graphics = self.native.CreateGraphics()
            graphics.DrawString(text, win_font, self.brush, float(x), float(y))
            graphics.Dispose()
        else:
            brush = Brush(self.pen.Color)
            graphics = self.native.CreateGraphics()
            graphics.DrawString(text, win_font, brush, float(x), float(y))
            graphics.Dispose()

    # Rehint

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
