import array
import datetime
import time
import traceback
from contextlib import contextmanager
from dataclasses import dataclass

import OpenGL

# Get spurious errors with Qt backend
OpenGL.ERROR_CHECKING = False

from OpenGL import GL  # noqa: E402

vertext_shader_source = """
#version 330 core

layout(location = 0) in vec4 position;

void main()
{
   gl_Position = position;
}
"""
fragment_shader_source = """
#version 330 core

uniform vec4 input_color = vec4(1.0, 0.0, 0.0, 1.0);

out vec4 output_color;
void main()
{
   output_color = input_color;
}
"""
FRAGMENT_SHADER_TEMPLATE = """#version 330 core

uniform vec3 iResolution;
uniform float iTime;
uniform float iTimeDelta;
uniform float iFrame;
uniform float iFrameRate;
uniform vec4 iMouse;
uniform vec4 iDate;

out vec4 output_color;

{source}

void main() {{
  mainImage(output_color, gl_FragCoord.xy);
}}
"""


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


RENDER_MESSAGE = """Rendering...
Frame: {iFrame[0]}
Frame rate: {iFrameRate[0]:.3f} fps

Resolution: {iResolution}
Mouse: {iMouse}

Time: {iTime[0]:.3f} s
Time delta: {iTimeDelta[0]:.3f} s
Date: {iDate[0]}-{iDate[1]}-{iDate[2]} {iDate[3]:.3f}

{deltas}
"""


class Renderer:
    source: str
    message: str

    def __init__(self, source):
        self.message = "Uninitialized."
        self.set_source(source)

    def set_source(self, source):
        self.fragment_shader_source = FRAGMENT_SHADER_TEMPLATE.format(source=source)
        self.source_updated = True

    def initialize_vbo(self, vertex_positions):
        self.vbo = Buffer(GL.GL_ARRAY_BUFFER, GL.GL_STATIC_DRAW)
        self.vbo.create()
        with self.vbo:
            self.vbo.set_data(vertex_positions)

    def initialize_program(self, vertex_shader_code, fragment_shader_code):
        self.program = Program(
            [
                Shader(GL.GL_VERTEX_SHADER, vertex_shader_code),
                Shader(GL.GL_FRAGMENT_SHADER, fragment_shader_code),
            ]
        )
        self.program.create()

    def initialize_vao(self, attribute):
        attribute_loc = self.program.attribute(attribute)
        self.vao = VertexArray()
        self.vao.create()
        with self.vao:
            with self.vbo:
                GL.glEnableVertexAttribArray(attribute_loc)
                GL.glVertexAttribPointer(0, 4, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

    def update_program(self):
        self.initialize_program(vertext_shader_source, self.fragment_shader_source)
        self.initialize_vao("position")
        self.start = time.time()
        self.timestamp = 0
        self.frame = 0
        self.deltas = []
        self.pointer = (0, 0)
        self.mouse_down = False
        self.drag_start = (0, 0)

    def on_init(self, widget, **kwargs):
        try:
            self.source_updated = False
            vertex_positions = bytes(
                array.array(
                    "f",
                    [
                        1.0,
                        1.0,
                        0.0,
                        1.0,  # triangle 1
                        1.0,
                        -1.0,
                        0.0,
                        1.0,
                        -1.0,
                        -1.0,
                        0.0,
                        1.0,
                        1.0,
                        1.0,
                        0.0,
                        1.0,  # triangle 2
                        -1.0,
                        -1.0,
                        0.0,
                        1.0,
                        -1.0,
                        1.0,
                        0.0,
                        1.0,
                    ],
                )
            )
            self.initialize_vbo(vertex_positions)
            self.update_program()
        except OpenGLError as exc:
            self.message = exc.args[0]
        except Exception:
            self.message = traceback.format_exc()
        else:
            self.message = "Initialization successful"

    def on_render(
        self,
        widget,
        size,
        pointer=(-1, -1),
        buttons=frozenset(),
        **kwargs,
    ):
        GL.glClearColor(0.0, 0.0, 1.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        if self.source_updated:
            try:
                self.program.delete()
                self.update_program()
            except OpenGLError as exc:
                self.message = exc.args[0]
                return
            except Exception:
                self.message = traceback.format_exc()
                return
            else:
                self.source_updated = False
                self.message = "Update successful"
                return

        try:
            n_vertices = 6
            if 0 <= pointer[0] < size[0] and 0 <= pointer[1] < size[1]:
                mouse_down = any(buttons)
                if mouse_down:
                    self.pointer = pointer
                    if not self.mouse_down:
                        # new mouse down
                        self.drag_start = pointer
                        self.mouse_down = True
                    elif self.drag_start[1] > 0:
                        # mouse was newly down, still down
                        self.drag_start = (self.drag_start[0], -self.drag_start[1])
                elif self.mouse_down:
                    # new mouse up
                    self.drag_start = (-self.drag_start[0], self.drag_start[1])
                    self.mouse_down = False

            t = time.time() - self.start
            self.deltas.append(t - self.timestamp + 1e-6)
            frame_rate = len(self.deltas) / sum(self.deltas)
            self.timestamp = t
            dt = datetime.datetime.now()

            uniforms = {
                "iResolution": (*size, 1.0),
                "iMouse": (*self.pointer, *self.drag_start),
                "iTime": (self.timestamp,),
                "iTimeDelta": (self.deltas[-1],),
                "iFrame": (self.frame,),
                "iFrameRate": (frame_rate,),
                "iDate": (
                    dt.year,
                    dt.month,
                    dt.day,
                    dt.hour * 3600
                    + dt.minute * 60
                    + dt.second
                    + (dt.microsecond / 1e6),
                ),
            }

            with self.program.use():
                with self.vao:
                    self.program.set_uniforms(uniforms)

                    GL.glDrawArrays(GL.GL_TRIANGLES, 0, n_vertices)

            self.frame += 1
            if len(self.deltas) > 100:
                del self.deltas[0]
        except Exception:
            self.message = traceback.format_exc()
            raise
        else:
            self.message = RENDER_MESSAGE.format(**uniforms, deltas=len(self.deltas))
