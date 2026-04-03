import os
from contextlib import contextmanager
from dataclasses import dataclass
from enum import IntEnum

import toga

if toga.backend in {"toga_cocoa", "toga_gtk", "toga_qt"}:
    if os.environ.get("TOGA_OPENGL") == "pyglet":
        from . import utils_pyglet as GL
    else:
        from . import utils_pyopengl as GL
elif toga.backend == "toga_android":
    from . import utils_android as GL
elif toga.backend == "toga_iOS":
    from . import utils_iOS as GL
else:
    raise RuntimeError("No OpenGL for backend.")


VERSION_HEADER = GL.VERSION_HEADER


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
        status = GL.glGetShaderiv(self.id, GL.GL_COMPILE_STATUS)
        if status == GL.GL_FALSE:
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
        status = GL.glGetProgramiv(self.id, GL.GL_LINK_STATUS)
        if status == GL.GL_FALSE:
            strInfoLog = GL.glGetProgramInfoLog(self.id)
            raise OpenGLError(f"Linker failure: \n{strInfoLog}")

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

    def active_uniforms(self):
        """Get information about the program's active uniforms.

        Returns a dictionary of uniform names mapping to the location, size,
        type and setter function of the attribute.
        """
        n_uniforms = GL.glGetProgramiv(self.id, GL.GL_ACTIVE_UNIFORMS)
        data = [GL.glGetActiveUniform(self.id, i) for i in range(n_uniforms)]
        uniforms = {
            name: (
                i,
                size,
                uniform_type,
                uniform_setters[uniform_type, size > 1],
            )
            for i, (name, size, uniform_type) in enumerate(data)
        }
        return uniforms

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
            GL.glVertexAttribPointer(loc, size, GL.GL_FLOAT, GL.GL_FALSE, 0, None)


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
        self.id = GL.glGenBuffers(1)
        self.set_data(data)

    def set_data(self, data):
        """Set data into a buffer.

        This automatically binds the buffer..
        """
        with self:
            GL.glBufferData(self.buffer_type, data, self.usage)

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
        self.id = GL.glGenVertexArrays(1)

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
