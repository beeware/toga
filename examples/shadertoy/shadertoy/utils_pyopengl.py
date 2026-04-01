from contextlib import contextmanager
from dataclasses import dataclass
from enum import IntEnum

import OpenGL

# Get spurious errors with Qt backend
OpenGL.ERROR_CHECKING = False

from OpenGL import GL  # noqa: E402


class ShaderType(IntEnum):
    vertex = GL.GL_VERTEX_SHADER
    fragment = GL.GL_FRAGMENT_SHADER


class BufferType(IntEnum):
    array = GL.GL_ARRAY_BUFFER


class BufferUsage(IntEnum):
    dynamic_draw = GL.GL_DYNAMIC_DRAW
    static_draw = GL.GL_STATIC_DRAW


uniform_setters = {
    (GL.GL_FLOAT, False): GL.glUniform1f,
    (GL.GL_FLOAT_VEC2, False): GL.glUniform2f,
    (GL.GL_FLOAT_VEC3, False): GL.glUniform3f,
    (GL.GL_FLOAT_VEC4, False): GL.glUniform4f,
    (GL.GL_FLOAT, True): GL.glUniform1fv,
    (GL.GL_FLOAT_VEC2, True): GL.glUniform2fv,
    (GL.GL_FLOAT_VEC3, True): GL.glUniform3fv,
    (GL.GL_FLOAT_VEC4, True): GL.glUniform4fv,
}


class OpenGLError(RuntimeError):
    pass


@dataclass
class Shader:
    shader_type: int
    source: str

    def create(self):
        self.id = GL.glCreateShader(self.shader_type)
        GL.glShaderSource(self.id, self.source)

        GL.glCompileShader(self.id)

        status = GL.glGetShaderiv(self.id, GL.GL_COMPILE_STATUS)
        if status == GL.GL_FALSE:
            info_log = GL.glGetShaderInfoLog(self.id).decode("utf-8")
            raise OpenGLError(
                f"Compilation failure for {self.shader_type} shader:\n{info_log}"
            )

    def delete(self):
        if hasattr(self, "id"):
            GL.glDeleteShader(self.id)
            del self.id


@dataclass
class Program:
    shaders: list[Shader]

    def create(self):
        for shader in self.shaders:
            shader.create()

        self.id = GL.glCreateProgram()

        for shader in self.shaders:
            GL.glAttachShader(self.id, shader.id)

        GL.glLinkProgram(self.id)

        status = GL.glGetProgramiv(self.id, GL.GL_LINK_STATUS)
        if status == GL.GL_FALSE:
            strInfoLog = GL.glGetProgramInfoLog(self.id).decode("utf-8")
            raise OpenGLError("Linker failure: \n" + strInfoLog)

        for shader in self.shaders:
            GL.glDetachShader(self.id, shader.id)

        for shader in self.shaders:
            shader.delete()

    def delete(self):
        if hasattr(self, "id"):
            GL.glDeleteProgram(self.id)
            del self.id

    @contextmanager
    def use(self):
        GL.glUseProgram(self.id)
        try:
            yield
        finally:
            GL.glUseProgram(0)

    def active_attributes(self):
        data = [
            GL.glGetActiveAttrib(self.id, i)
            for i in range(GL.glGetProgramiv(self.id, GL.GL_ACTIVE_ATTRIBUTES))
        ]
        return {
            name.decode("utf-8"): (i, size, uniform_type)
            for i, (name, size, uniform_type) in enumerate(data)
        }

    def active_uniforms(self):
        data = [
            GL.glGetActiveUniform(self.id, i)
            for i in range(GL.glGetProgramiv(self.id, GL.GL_ACTIVE_UNIFORMS))
        ]
        return {
            name.decode("utf-8"): (
                i,
                size,
                uniform_type,
                uniform_setters[uniform_type, size > 1],
            )
            for i, (name, size, uniform_type) in enumerate(data)
        }

    def attribute(self, item):
        return GL.glGetAttribLocation(self.id, item)

    def set_uniforms(self, uniforms):
        for uniform, (loc, size, _, setter) in self.active_uniforms().items():
            if uniform in uniforms:
                if size == 1:
                    setter(loc, *uniforms[uniform])
                else:
                    setter(loc, size, uniforms[uniform])


@dataclass
class Buffer:
    buffer_type: int
    usage: int

    def create(self):
        self.id = GL.glGenBuffers(1)

    def set_data(self, data):
        GL.glBufferData(self.buffer_type, data, self.usage)

    def bind(self):
        GL.glBindBuffer(self.buffer_type, self.id)

    def unbind(self):
        GL.glBindBuffer(self.buffer_type, 0)

    def __enter__(self):
        self.bind()

    def __exit__(self, exc_type, exc_value, traceback):
        self.unbind()
        return False


@dataclass
class VertexArray:
    def create(self):
        self.id = GL.glGenVertexArrays(1)

    def bind(self):
        GL.glBindVertexArray(self.id)

    def unbind(self):
        GL.glBindVertexArray(0)

    def __enter__(self):
        self.bind()

    def __exit__(self, exc_type, exc_value, traceback):
        self.unbind()
        return False
