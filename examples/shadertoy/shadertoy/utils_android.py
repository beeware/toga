from contextlib import contextmanager
from dataclasses import dataclass
from enum import IntEnum

from android.opengl import GLES32 as GL
from java import jarray, jbyte, jint
from java.nio import ByteBuffer, ByteOrder


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

        status_p = jarray(jint)([0])
        GL.glGetShaderiv(self.id, GL.GL_COMPILE_STATUS, status_p, 0)
        status = status_p[0]
        if not status:
            info_log = GL.glGetShaderInfoLog(self.id)
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

        status_p = jarray(jint)([0])
        GL.glGetProgramiv(self.id, GL.GL_LINK_STATUS, status_p, 0)
        status = status_p[0]
        if not status:
            strInfoLog = GL.glGetProgramInfoLog(self.id)
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
        param = jarray(jint)([0])
        GL.glGetProgramiv(self.id, GL.GL_ACTIVE_UNIFORMS, param, 0)
        n_uniforms = param[0]

        data = {}
        for i in range(n_uniforms):
            length = jarray(jint)([0])
            size = jarray(jint)([0])
            type = jarray(jint)([0])
            name = jarray(jbyte)(b"\0x00" * 255)
            GL.glGetActiveUniform(
                self.id,
                i,
                255,
                length,
                0,
                size,
                0,
                type,
                0,
                name,
                0,
            )
            data[bytes(name[: length[0]]).decode("utf-8")] = (
                i,
                size[0],
                type[0],
                uniform_setters[type[0], size[0] > 1],
            )
        return data

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
        buffers = jarray(jint)([0])
        GL.glGenBuffers(1, buffers, 0)
        self.id = buffers[0]

    def set_data(self, data):
        nbytes = len(data)
        buffer = ByteBuffer.allocateDirect(nbytes)
        buffer.order(ByteOrder.nativeOrder())
        buffer.put(data)
        buffer.position(0)
        GL.glBufferData(self.buffer_type, nbytes, buffer, self.usage)

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
        buffers = jarray(jint)([0])
        GL.glGenVertexArrays(1, buffers, 0)
        self.id = buffers[0]

    def bind(self):
        GL.glBindVertexArray(self.id)

    def unbind(self):
        GL.glBindVertexArray(0)

    def __enter__(self):
        self.bind()

    def __exit__(self, exc_type, exc_value, traceback):
        self.unbind()
        return False
