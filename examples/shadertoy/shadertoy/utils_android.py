"""Utility objects and methods for PyOpenGL"""

from contextlib import contextmanager
from dataclasses import dataclass
from enum import IntEnum

from android.opengl import GLES32 as GL
from java import jarray, jbyte, jint
from java.nio import ByteBuffer, ByteOrder

#: Shader version header: we want OpenGL ES GLSL 3
VERSION_HEADER = """#version 300 es"""


class ShaderType(IntEnum):
    """Enum for the different OpenGL shader types."""

    vertex = GL.GL_VERTEX_SHADER
    fragment = GL.GL_FRAGMENT_SHADER


class BufferType(IntEnum):
    """Enum for the different OpenGL buffer types."""

    array = GL.GL_ARRAY_BUFFER


class BufferUsage(IntEnum):
    """Enum for the different OpenGL buffer usage hints."""

    dynamic_draw = GL.GL_DYNAMIC_DRAW
    static_draw = GL.GL_STATIC_DRAW


#: Map from OpenGL data types to corresponding setter functions
#: This is far from complete.
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
    """OpenGL-specific runtime errors."""

    pass


def v_func(v_size=1, jtype=jint):
    """Decorator for functions expecting a pointer to an output vector.

    A number of OpenGL functions have a suffix of the form {l}{t}v,
    which expect an argument of an array of length l of type t (and
    an offset into it) which is used to return values by setting them
    into the array.

    This wrapper wraps these functions to create a java array of the
    correct type, call the function, and then unpack the values from
    the array.
    """

    def wrapper(func):
        def call_v_function(*args, v_size=1, jtype=jint):
            data = jarray(jtype)([0] * v_size)
            func(*args, data, 0)
            if v_size == 1:
                return data[0]
            else:
                return tuple(data)

        return call_v_function

    return wrapper


glGetShader = v_func()(GL.glGetShaderiv)
glGetProgram = v_func()(GL.glGetProgramiv)
glGenBuffer = v_func()(GL.glGenBuffers)
glGenVertexArray = v_func()(GL.glGenVertexArrays)


@dataclass
class Shader:
    """A dataclass that encapsulates an OpenGL shader."""

    shader_type: int
    source: str

    def create(self):
        """Create and compile the shader."""
        self.id = GL.glCreateShader(self.shader_type)
        GL.glShaderSource(self.id, self.source)

        GL.glCompileShader(self.id)

        # Handle errors
        status = glGetShader(self.id, GL.GL_COMPILE_STATUS)
        if not status:
            info_log = GL.glGetShaderInfoLog(self.id)
            raise OpenGLError(
                f"Compilation failure for {self.shader_type} shader:\n{info_log}"
            )

    def delete(self):
        """Delete the shader."""
        if hasattr(self, "id"):
            GL.glDeleteShader(self.id)
            del self.id


@dataclass
class Program:
    """A dataclass that encapsulates an OpenGL program."""

    shaders: list[Shader]

    def create(self):
        """Create the program and its shaders and link them."""
        for shader in self.shaders:
            shader.create()

        self.id = GL.glCreateProgram()

        for shader in self.shaders:
            GL.glAttachShader(self.id, shader.id)

        GL.glLinkProgram(self.id)

        # Handle errors
        status = glGetProgram(self.id, GL.GL_LINK_STATUS)
        if not status:
            strInfoLog = GL.glGetProgramInfoLog(self.id)
            raise OpenGLError("Linker failure: \n" + strInfoLog)

        # clean up shaders
        for shader in self.shaders:
            GL.glDetachShader(self.id, shader.id)
        for shader in self.shaders:
            shader.delete()

    def delete(self):
        """Delete the program."""
        if hasattr(self, "id"):
            GL.glDeleteProgram(self.id)
            del self.id

    @contextmanager
    def use(self):
        """Context manager that sets the program for use and resets it when done."""
        GL.glUseProgram(self.id)
        try:
            yield
        finally:
            GL.glUseProgram(0)

    def active_attributes(self):
        """Get information about the program's active attributes.

        Returns a dictionary of attribute names mapping to the location, size and
        type of the attribute.
        """
        data = [
            GL.glGetActiveAttrib(self.id, i)
            for i in range(GL.glGetProgramiv(self.id, GL.GL_ACTIVE_ATTRIBUTES))
        ]
        return {
            name.decode("utf-8"): (i, size, uniform_type)
            for i, (name, size, uniform_type) in enumerate(data)
        }

    def active_uniforms(self):
        """Get information about the program's active uniforms.

        Returns a dictionary of uniform names mapping to the location, size,
        type and setter function of the attribute.
        """
        n_uniforms = glGetProgram(self.id, GL.GL_ACTIVE_UNIFORMS)

        data = {}
        for i in range(n_uniforms):
            # Need to get values out via Java arrays
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
        """Return the location of an active attribute."""
        return GL.glGetAttribLocation(self.id, item)

    def set_uniforms(self, uniforms):
        """Set the values of active uniforms from a dictionary of values."""
        for uniform, (loc, size, _, setter) in self.active_uniforms().items():
            if uniform in uniforms:
                if size == 1:
                    setter(loc, *uniforms[uniform])
                else:
                    setter(loc, size, uniforms[uniform])

    def bind_attribute_buffer(self, attribute, vbo, *, size=4):
        """Bind an active attribute to a vertex buffer object."""
        loc = self.attribute(attribute)
        with vbo:
            GL.glEnableVertexAttribArray(loc)
            GL.glVertexAttribPointer(loc, size, GL.GL_FLOAT, False, 0, 0)


@dataclass
class Buffer:
    """A dataclass that encapsulates an OpenGL buffer.

    This can be used as a context manager to automatically bind and unbind
    the buffer for use.
    """

    buffer_type: int
    usage: int

    def create(self, data):
        """Generate a new buffer and set the data into it."""
        self.id = glGenBuffer(1)
        self.set_data(data)

    def set_data(self, data):
        """Set data into a buffer.

        This automatically binds the buffer.
        """
        nbytes = len(data)
        buffer = ByteBuffer.allocateDirect(nbytes)
        buffer.order(ByteOrder.nativeOrder())
        buffer.put(data)
        buffer.position(0)
        with self:
            GL.glBufferData(self.buffer_type, nbytes, buffer, self.usage)

    def bind(self):
        """Bind the buffer so that it is the current buffer."""
        GL.glBindBuffer(self.buffer_type, self.id)

    def unbind(self):
        """Unbind the buffer so that it is no longer the current buffer."""
        GL.glBindBuffer(self.buffer_type, 0)

    def __enter__(self):
        """Enter the context manager, binding the buffer."""
        self.bind()

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context manager, unbinding the buffer."""
        self.unbind()
        return False


@dataclass
class VertexArrayObject:
    """A dataclass that encapsulates an OpenGL vertex array object.

    This can be used as a context manager to automatically bind and unbind
    the vertex array object for use.
    """

    def create(self):
        """Generate a new vertex array object."""
        self.id = glGenVertexArray(1)

    def bind(self):
        """Make the vertex array object the current vertex array object."""
        GL.glBindVertexArray(self.id)

    def unbind(self):
        """Make the vertex array object no longer the current vertex array object."""
        GL.glBindVertexArray(0)

    def __enter__(self):
        """Enter the context manager, binding the vertex array object."""
        self.bind()

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context manager, unbinding the vertex array object."""
        self.unbind()
        return False
