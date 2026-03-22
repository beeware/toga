import ctypes
from ctypes import c_float, cdll
from ctypes.util import find_library

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

# possibly use PyOpenGL instead?
GL = cdll.LoadLibrary(find_library("OpenGL"))


class CocoaOpenGLContext(OpenGLContext):
    def clear_color(self, r: float, g: float, b: float, a: float):
        GL.glClearColor(c_float(r), c_float(g), c_float(b), c_float(a))

    def clear(self, mask: int):
        GL.glClear(mask)

    def create_shader(self, type: int):
        return GL.glCreateShader(type)

    def shader_source(self, shader: int, source: str):
        GL.glShaderSource(shader, source)

    def compile_shader(self, shader: int):
        GL.glCompileShader(shader)

    def delete_shader(self, shader: int):
        GL.glDeleteShader(shader)

    def create_program(self) -> int:
        return GL.glCreateProgram()

    def attach_shader(self, program: int, shader: int):
        GL.glAttachShader(program, shader)

    def link_program(self, program: int):
        GL.glLinkProgram(program)

    def delete_program(self, program):
        GL.glDeleteProgram(program)


class TogaOpenGLView(NSOpenGLView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def drawRect_(self, rect: NSRect) -> None:
        self.openGLContext.makeCurrentContext()
        context = self.openGLContext
        GL.glViewport(0, 0, int(rect.size.width), int(rect.size.height))
        self.interface.on_render(CocoaOpenGLContext())
        context.flushBuffer()

    @objc_method
    def initWithFrame_(self, frame: NSRect):
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
        pixel_format = NSOpenGLPixelFormat.alloc().initWithAttributes_(attributes)
        return self.initWithFrame_pixelFormat_(frame, pixel_format)


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
