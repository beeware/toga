from collections.abc import Sequence
from copy import copy
from dataclasses import dataclass
from math import ceil

from rubicon.objc import (
    Block,
    CGFloat,
    CGRect,
    CGSize,
    NSMutableDictionary,
    NSPoint,
    NSRect,
    NSSize,
    objc_id,
    objc_method,
    objc_property,
)
from travertino.size import at_least

from toga.colors import BLACK, TRANSPARENT, Color
from toga.constants import Baseline, FillRule
from toga.widgets.canvas.geometry import round_rect
from toga_iOS.colors import native_color
from toga_iOS.images import nsdata_to_bytes
from toga_iOS.libs import (
    CGPathDrawingMode,
    CGRectMake,
    NSAttributedString,
    NSFontAttributeName,
    NSForegroundColorAttributeName,
    NSStrokeColorAttributeName,
    NSStrokeWidthAttributeName,
    UIColor,
    UIGraphicsImageRenderer,
    UIView,
    core_graphics,
    kCGPathEOFill,
    kCGPathFill,
    kCGPathStroke,
    uikit,
)
from toga_iOS.widgets.base import Widget


@dataclass(slots=True)
class State:
    # Core graphics holds onto its own state, which works great, except we need to hold
    # onto these values in order to fill or stroke text.
    fill_style: Color = Color.parse(BLACK)
    line_dash: Sequence[float] = ()
    line_width: float = 2.0
    stroke_style: Color = Color.parse(BLACK)


class Context:
    def __init__(self, impl):
        self.impl = impl
        self.native = uikit.UIGraphicsGetCurrentContext()
        self.states = [State()]
        self.set_line_width(2.0)

        # Backwards compatibility for Toga <= 0.5.3
        self.in_fill = False
        self.in_stroke = False

    @property
    def state(self):
        return self.states[-1]

    # Context management
    def save(self):
        core_graphics.CGContextSaveGState(self.native)
        self.states.append(copy(self.state))

    def restore(self):
        core_graphics.CGContextRestoreGState(self.native)
        self.states.pop()

    # Setting attributes
    def set_fill_style(self, color):
        core_graphics.CGContextSetRGBFillColor(
            self.native, color.r / 255, color.g / 255, color.b / 255, color.a
        )
        self.state.fill_style = color

    def set_line_dash(self, line_dash):
        core_graphics.CGContextSetLineDash(
            self.native,
            0,
            (CGFloat * len(line_dash))(*line_dash),
            len(line_dash),
        )
        self.state.line_dash = line_dash

    def set_line_width(self, line_width):
        core_graphics.CGContextSetLineWidth(self.native, line_width)
        self.state.line_width = line_width

    def set_stroke_style(self, color):
        core_graphics.CGContextSetRGBStrokeColor(
            self.native, color.r / 255, color.g / 255, color.b / 255, color.a
        )
        self.state.stroke_style = color

    # Basic paths
    def begin_path(self):
        core_graphics.CGContextBeginPath(self.native)

    def close_path(self):
        core_graphics.CGContextClosePath(self.native)

    def move_to(self, x, y):
        core_graphics.CGContextMoveToPoint(self.native, x, y)

    def line_to(self, x, y):
        self._ensure_subpath(x, y)
        core_graphics.CGContextAddLineToPoint(self.native, x, y)

    def _ensure_subpath(self, x, y):
        if core_graphics.CGContextIsPathEmpty(self.native):
            self.move_to(x, y)

    # Basic shapes

    def bezier_curve_to(
        self,
        cp1x,
        cp1y,
        cp2x,
        cp2y,
        x,
        y,
    ):
        self._ensure_subpath(cp1x, cp1y)
        core_graphics.CGContextAddCurveToPoint(
            self.native, cp1x, cp1y, cp2x, cp2y, x, y
        )

    def quadratic_curve_to(self, cpx, cpy, x, y):
        self._ensure_subpath(cpx, cpy)
        core_graphics.CGContextAddQuadCurveToPoint(self.native, cpx, cpy, x, y)

    def arc(
        self,
        x,
        y,
        radius,
        startangle,
        endangle,
        counterclockwise,
    ):
        # UIKit uses a flipped coordinate system, so clockwise
        # is actually counterclockwise
        if counterclockwise:
            clockwise = 1
        else:
            clockwise = 0
        core_graphics.CGContextAddArc(
            self.native, x, y, radius, startangle, endangle, clockwise
        )

    def ellipse(
        self,
        x,
        y,
        radiusx,
        radiusy,
        rotation,
        startangle,
        endangle,
        counterclockwise,
    ):
        self.save()
        self.translate(x, y)
        self.rotate(rotation)
        self.scale(radiusx, radiusy)
        self.arc(0, 0, 1.0, startangle, endangle, counterclockwise)
        self.restore()

    def rect(self, x, y, width, height):
        rectangle = CGRectMake(x, y, width, height)
        core_graphics.CGContextAddRect(self.native, rectangle)

    def round_rect(self, x, y, width, height, radii):
        round_rect(self, x, y, width, height, radii)

    # Drawing Paths
    def fill(self, fill_rule):
        if fill_rule == FillRule.EVENODD:
            mode = CGPathDrawingMode(kCGPathEOFill)
        else:
            mode = CGPathDrawingMode(kCGPathFill)
        if not core_graphics.CGContextIsPathEmpty(self.native):
            path = core_graphics.CGContextCopyPath(self.native)
            core_graphics.CGContextDrawPath(self.native, mode)
            core_graphics.CGContextAddPath(self.native, path)

    def stroke(self):
        mode = CGPathDrawingMode(kCGPathStroke)

        if not core_graphics.CGContextIsPathEmpty(self.native):
            path = core_graphics.CGContextCopyPath(self.native)
            core_graphics.CGContextDrawPath(self.native, mode)
            core_graphics.CGContextAddPath(self.native, path)

    # Transformations
    def rotate(self, radians):
        core_graphics.CGContextRotateCTM(self.native, radians)

    def scale(self, sx, sy):
        core_graphics.CGContextScaleCTM(self.native, sx, sy)

    def translate(self, tx, ty):
        core_graphics.CGContextTranslateCTM(self.native, tx, ty)

    def reset_transform(self):
        # Restore the "clean" state of the graphics context.
        core_graphics.CGContextRestoreGState(self.native)
        # CoreGraphics has a stack-based state representation,
        # so ensure that there is a new, clean version of the "clean"
        # state on the stack.
        core_graphics.CGContextSaveGState(self.native)

    # Text

    def write_text(self, text, x, y, font, baseline, line_height):
        lines = text.splitlines()
        scaled_line_height = self.impl._line_height(font, line_height)
        total_height = scaled_line_height * len(lines)

        if baseline == Baseline.TOP:
            top = y + font.native.ascender
        elif baseline == Baseline.MIDDLE:
            top = y + font.native.ascender - (total_height / 2)
        elif baseline == Baseline.BOTTOM:
            top = y + font.native.ascender - total_height
        else:
            # Default to Baseline.ALPHABETIC
            top = y

        for line_num, line in enumerate(lines):
            # Rounding minimizes differences between scale factors.
            origin = NSPoint(round(x), round(top) + (scaled_line_height * line_num))
            kwargs = {}
            if self.in_fill:
                kwargs |= {"fill_style": self.state.fill_style}
            if self.in_stroke:
                kwargs |= {
                    "stroke_style": self.state.stroke_style,
                    "line_width": self.state.line_width,
                    # Current implementation doesn't respect line dash; should this?
                }
            rs = self.impl._render_string(line, font, **kwargs)

            # "This method uses the baseline origin by default. If
            # NSStringDrawingUsesLineFragmentOrigin is not specified, the
            # rectangle’s height will be ignored"
            #
            # Previously we used drawAtPoint, which takes a TOP-relative origin. But
            # this often gave off-by-one errors in ALPHABETIC mode, even when we
            # attempted to put the baseline on a logical pixel edge. This may be
            # because drawAtPoint calculates the line height in its own way and then
            # sets the baseline relative to its bottom
            # (https://www.sketch.com/blog/typesetting-in-sketch/), but it would be
            # unwise to rely on that.
            rs.drawWithRect(
                NSRect(origin, NSSize(2**31 - 1, 0)), options=0, context=None
            )

    # Images
    def draw_image(self, image, x, y, width, height):
        ui_image = image._impl.native

        # Have an UIImage, need a CGImage
        cg_image = ui_image.CGImage

        # Quartz is flipped relative to data, so we:
        # - store the current state
        # - translate to bottom of the image
        # - flip vertical axis
        # - draw image at the new y-origin, with normal height
        # - restore state
        core_graphics.CGContextSaveGState(self.native)
        core_graphics.CGContextTranslateCTM(self.native, 0, y + height)
        core_graphics.CGContextScaleCTM(self.native, 1.0, -1.0)
        rectangle = CGRectMake(x, 0, width, height)
        core_graphics.CGContextDrawImage(self.native, rectangle, cg_image)
        core_graphics.CGContextRestoreGState(self.native)


class TogaCanvas(UIView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def drawRect_(self, rect: CGRect) -> None:
        self.interface.root_state._draw(Context(self.impl))

    @objc_method
    def touchesBegan_withEvent_(self, touches, event) -> None:
        position = touches.allObjects()[0].locationInView(self)
        self.interface.on_press(position.x, position.y)

    @objc_method
    def touchesMoved_withEvent_(self, touches, event) -> None:
        position = touches.allObjects()[0].locationInView(self)
        self.interface.on_drag(position.x, position.y)

    @objc_method
    def touchesEnded_withEvent_(self, touches, event) -> None:
        position = touches.allObjects()[0].locationInView(self)
        self.interface.on_release(position.x, position.y)


class Canvas(Widget):
    def create(self):
        self.native = TogaCanvas.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        # Add the layout constraints
        self.add_constraints()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self.interface.on_resize(width=width, height=height)

    def redraw(self):
        self.native.setNeedsDisplay()

    def set_background_color(self, color):
        if color == TRANSPARENT or color is None:
            self.native.backgroundColor = UIColor.clearColor
        else:
            self.native.backgroundColor = native_color(color)

    # Text
    def _render_string(
        self,
        text,
        font,
        fill_style=None,
        stroke_style=None,
        line_width=2.0,
    ):
        textAttributes = NSMutableDictionary.alloc().init()
        textAttributes[NSFontAttributeName] = font.native

        if stroke_style:
            textAttributes[NSStrokeColorAttributeName] = native_color(stroke_style)
            # Stroke width is expressed as a percentage of the font size, or a negative
            # percentage to get both stroke and fill.
            stroke_width = line_width / font.native.pointSize * 100
            if fill_style:
                stroke_width *= -1
            textAttributes[NSStrokeWidthAttributeName] = stroke_width

        if fill_style:
            textAttributes[NSForegroundColorAttributeName] = native_color(fill_style)

        text_string = NSAttributedString.alloc().initWithString(
            text, attributes=textAttributes
        )
        return text_string

    # Although the native API can measure and draw multi-line strings, this makes the
    # line spacing depend on the scale factor, which messes up the tests.
    def _line_height(self, font, line_height):
        if line_height is None:
            # descender is a negative number.
            return ceil(font.native.ascender - font.native.descender)
        else:
            return font.native.pointSize * line_height

    def measure_text(self, text, font, line_height):
        # We need at least a fill color to render, but that won't change the size.
        sizes = [
            self._render_string(line, font, fill_style=Color.parse(BLACK)).size()
            for line in text.splitlines()
        ]
        return (
            ceil(max(size.width for size in sizes)),
            self._line_height(font, line_height) * len(sizes),
        )

    def get_image_data(self):
        renderer = UIGraphicsImageRenderer.alloc().initWithSize(self.native.bounds.size)

        def render(context):
            self.native.drawViewHierarchyInRect(
                self.native.bounds, afterScreenUpdates=True
            )

        return nsdata_to_bytes(
            renderer.PNGDataWithActions(Block(render, None, objc_id))
        )

    # Rehint
    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = at_least(fitting_size.height)
