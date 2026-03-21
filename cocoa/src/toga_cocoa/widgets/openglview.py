import ctypes
import ctypes.util

from rubicon.objc import NSMakeRect, objc_method
from travertino.size import at_least

from toga.widgets.gl.openglcontext import OpenGLContext
from toga_cocoa.libs import (
    NSOpenGLPFAAccelerated,
    NSOpenGLPFAAccumSize,
    NSOpenGLPFAAlphaSize,
    NSOpenGLPFAColorSize,
    NSOpenGLPFADepthSize,
    NSOpenGLPFADoubleBuffer,
    NSOpenGLPFANoRecovery,
    NSOpenGLPFAOpenGLProfile,
    NSOpenGLPFAStencilSize,
    NSOpenGLPFAWindow,
    NSOpenGLPixelFormat,
    NSOpenGLProfileVersion4_1Core,
    NSOpenGLView,
    NSRect,
)

from .base import Widget

# possibly use PyOpenGL instead?
GL = ctypes.cdll.LoadLibrary(ctypes.util.find_library("OpenGL"))


class CocoaOpenGLContext(OpenGLContext):
    def __init__(self, impl):
        self.impl = impl
        self.native = impl.native.openGLContext

    def clear_color(self, r: float, g: float, b: float, a: float):
        GL.glClearColor(
            ctypes.c_float(r), ctypes.c_float(g), ctypes.c_float(b), ctypes.c_float(a)
        )
        print("here")

    def clear(self, mask: int):
        GL.glClear(mask)


class TogaOpenGLView(NSOpenGLView):
    # interface = objc_property(object, weak=True)
    # impl = objc_property(object, weak=True)

    @objc_method
    def drawRect_(self, rect: NSRect) -> None:
        self.openGLContext.makeCurrentContext()
        context = self.openGLContext
        GL.glViewport(0, 0, int(rect.size.width), int(rect.size.height))
        GL.glClearColor(
            ctypes.c_float(1.0),
            ctypes.c_float(0.0),
            ctypes.c_float(0.0),
            ctypes.c_float(1.0),
        )
        GL.glClear(0x00004000)
        context.flushBuffer()

    @objc_method
    def initWithFrame(self, frame: NSRect):
        # XXX This doesn't seem to be being called?
        a = (
            NSOpenGLPFANoRecovery,
            NSOpenGLPFAWindow,
            NSOpenGLPFAAccelerated,
            NSOpenGLPFADoubleBuffer,
            NSOpenGLPFAColorSize,
            24,
            NSOpenGLPFAAlphaSize,
            8,
            NSOpenGLPFADepthSize,
            24,
            NSOpenGLPFAStencilSize,
            8,
            NSOpenGLPFAAccumSize,
            NSOpenGLPFAOpenGLProfile,
            NSOpenGLProfileVersion4_1Core,
            0,
        )
        attributes = (ctypes.c_uint32 * len(a))(*a)
        pixel_format = NSOpenGLPixelFormat.alloc().initWithAttributes(attributes)
        return self.initWithFrame_pixelFormat(frame, pixel_format)


class OpenGLView(Widget):
    def create(self):
        # XXX This doesn't seem quite right - rect is arbitrary, but don't know size yet
        rect = NSMakeRect(0, 0, 500, 200)
        self.native = TogaOpenGLView.alloc().initWithFrame(rect)
        self.native.interface = self.interface
        self.native.impl = self

        # Add the layout constraints
        self.add_constraints()

    def redraw(self):
        self.native.needsDisplay = True

    # Rehint
    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.intrinsic.height = at_least(fitting_size.height)
        self.interface.intrinsic.width = at_least(fitting_size.width)
