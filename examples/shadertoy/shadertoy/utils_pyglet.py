"""Utility objects and methods for Pyglet"""

from ctypes import POINTER, byref, c_char, c_char_p, c_int, cast, create_string_buffer

from pyglet.gl import gl as GL

#: Shader version header: this should work on most modern desktops
VERSION_HEADER = "#version 330 core"

# Adapt some functions to common API


def glShaderSource(id, source):
    source_bytes = source.encode("utf-8")
    GL.glShaderSource(
        id,
        1,
        cast(c_char_p(source_bytes), POINTER(c_char)),
        c_int(len(source_bytes)),
    )


def glGetShaderiv(id, param):
    status = c_int(0)
    GL.glGetShaderiv(id, param, byref(status))
    return status.value


def glGetShaderInfoLog(id):
    raise NotImplementedError()


def glGetProgramiv(id, param):
    status = c_int(0)
    GL.glGetProgramiv(id, param, byref(status))
    return status.value


def glGetProgramInfoLog(id):
    raise NotImplementedError()


def glGetActiveUniform(id, loc):
    size = GL.GLint()
    uniform_type = GL.GLenum()
    buf_size = 192
    name = create_string_buffer(buf_size)
    GL.glGetActiveUniform(id, loc, buf_size, None, size, uniform_type, name)
    return name.value.decode("utf-8"), size.value, uniform_type.value


def glGetAttribLocation(id, attrib):
    buffer = create_string_buffer(attrib.encode("utf-8"))
    return GL.glGetAttribLocation(id, buffer)


def glBufferData(buffer_type, data: bytes, usage):
    GL.glBufferData(buffer_type, GL.GLsizeiptr(len(data)), data, usage)


def glGenBuffers(n):
    if n == 1:
        buffer_id = GL.GLuint()
        GL.glGenBuffers(n, buffer_id)
        return buffer_id.value
    else:
        raise NotImplementedError()


def glGenVertexArrays(n):
    if n == 1:
        id = GL.GLuint()
        GL.glGenVertexArrays(1, id)
        return id.value
    else:
        raise NotImplementedError()


def __getattr__(name):
    value = getattr(GL, name, None)
    if value is not None:
        globals()[name] = value
        return value
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
