import ctypes

import moderngl
from OpenGL import GL
from rubicon.objc import objc_method, objc_property
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
    NSOpenGLPFAStencilSize,
    NSOpenGLPFAWindow,
    NSOpenGLPixelFormat,
    NSOpenGLView,
    NSRect,
)

from .base import Widget


class CocoaOpenGLContext(OpenGLContext):
    def __init__(self, impl):
        self.impl = impl
        self.native = impl.native.openGLContext
        print(self.native)

    def clear_color(self, r: float, g: float, b: float, a: float):
        GL.glClearColor(r, g, b, a)
        print("here")

    def clear(self, mask: int):
        GL.glClear(mask)
        print("and here")


class TogaOpenGLView(NSOpenGLView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def drawRect_(self, rect: NSRect) -> None:
        self.openGLContext.makeCurrentContext()
        context = moderngl.create_context()
        context.clear(1.0, 0.0, 0.0, 1.0)
        # context = CocoaOpenGLContext(self.impl)
        # context.native.makeCurrentContext()
        # GL.glViewport(0, 0, int(rect.size.width), int(rect.size.height))
        # GL.glClearColor(1.0, 0.0, 0.0, 1.0)
        # GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        # print('here')
        # # self.interface.on_render(context)
        self.openGLContext.flushBuffer()

    @objc_method
    def initWithFrame(self, frame: NSRect):
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
            0,
        )
        attributes = (ctypes.c_uint32 * len(a))(*a)
        pixel_format = NSOpenGLPixelFormat.alloc().initWithAttributes(attributes)
        self.initWithFrame_pixelFormat(frame, pixel_format)


class OpenGLView(Widget):
    def create(self):
        self.native = TogaOpenGLView.alloc().init()
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
