from android.opengl import GLES20 as GL, GLSurfaceView
from java import dynamic_proxy

from toga.widgets.gl.openglcontext import OpenGLContext

from .base import Widget


class AndroidOpenGLContext(OpenGLContext):
    """The implementation layer of a Qt OpenGL context."""

    def clear_color(self, r: float, g: float, b: float, a: float):
        GL.glClearColor(r, g, b, a)

    def clear(self, mask: int):
        GL.glClear(mask)

    def create_shader(self, type: int):
        return GL.glCreateShader(type)

    def shader_source(self, shader: int, source: str):
        GL.glShaderSource(shader, source)

    def compile_shader(self, shader: int):
        GL.glCompileShader(shader)

    def delete_shader(self, shader):
        GL.glDeleteShader(shader)

    def create_program(self) -> int:
        return GL.glCreateProgram()

    def attach_shader(self, program: int, shader: int):
        GL.glAttachShader(program, shader)

    def link_program(self, program: int):
        GL.glLinkProgram(program)

    def delete_program(self, program):
        GL.glDeleteProgram(program)


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
