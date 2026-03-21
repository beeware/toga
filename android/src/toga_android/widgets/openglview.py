from android.opengl import GLES20 as GL, GLSurfaceView
from java import dynamic_proxy

from toga.widgets.gl.openglcontext import OpenGLContext

from .base import Widget


class AndroidOpenGLContext(OpenGLContext):
    """The implementation layer of a Qt OpenGL context."""

    def __init__(self):
        self.native = GL

    def clear_color(self, r: float, g: float, b: float, a: float):
        self.native.glClearColor(r, g, b, a)

    def clear(self, mask: int):
        self.native.glClear(mask)

    def create_shader(self, type: int):
        return self.native.glCreateShader(type)

    def shader_source(self, shader: int, source: str):
        self.native.glShaderSource(shader, source)

    def compile_shader(self, shader: int):
        self.native.glCompileShader(shader)

    def delete_shader(self, shader):
        self.native.glDeleteShader(shader)

    def create_program(self) -> int:
        return self.native.glCreateProgram()

    def attach_shader(self, program: int, shader: int):
        self.native.glAttachShader(program, shader)

    def link_program(self, program: int):
        self.native.glLinkProgram(program)

    def delete_program(self, program):
        self.native.glDeleteProgram(program)


class TogaGLRenderer(dynamic_proxy(GLSurfaceView.Renderer)):
    def onSurfaceCreated(self, unused, config):
        pass

    def onDrawFrame(self, unused):
        self._redraw()

    def onSurfaceChanged(self, unused, width, height):
        self._redraw()

    def _redraw(self):
        context = AndroidOpenGLContext()
        self.interface.on_render(context)


class OpenGLView(Widget):
    def create(self):
        self.native = GLSurfaceView(self._native_activity)
        self.renderer = TogaGLRenderer()
        self.renderer.interface = self.interface
        self.native.setEGLContextClientVersion(2)
        self.native.setRenderer(self.renderer)

    def redraw(self):
        self.native.invalidate()
