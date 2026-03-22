from ctypes import c_float

from rubicon.objc import objc_method, objc_property
from travertino.size import at_least

from toga.widgets.gl.openglcontext import OpenGLContext
from toga_iOS.libs import (
    CGRect,
    CGSize,
    EAGLContext,
    GLKView,
    GLKViewDrawableColorFormatRGBA8888,
    GLKViewDrawableDepthFormat24,
    GLKViewDrawableMultisample4X,
    GLKViewDrawableStencilFormat8,
    kEAGLRenderingAPIOpenGLES2,
    opengles as GL,
)

from .base import Widget


class iOSOpenGLContext(OpenGLContext):
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


class TogaGLKView(GLKView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def drawRect_(self, rect: CGRect) -> None:
        self.interface.on_render(iOSOpenGLContext())


class OpenGLView(Widget):
    def create(self):
        self.native = TogaGLKView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.context = EAGLContext.alloc().initWithAPI_(
            kEAGLRenderingAPIOpenGLES2
        )

        # # Configure renderbuffers created by the view
        self.native.drawableColorFormat = GLKViewDrawableColorFormatRGBA8888
        self.native.drawableDepthFormat = GLKViewDrawableDepthFormat24
        self.native.drawableStencilFormat = GLKViewDrawableStencilFormat8

        # # Enable multisampling
        self.native.drawableMultisample = GLKViewDrawableMultisample4X

        # Add the layout constraints
        self.add_constraints()

    def redraw(self):
        self.native.needsDisplay = True

    # Rehint
    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = at_least(fitting_size.height)
