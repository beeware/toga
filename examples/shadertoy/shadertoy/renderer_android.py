import array
import datetime
import time
import traceback

from .utils_android import (
    GL,
    Buffer,
    BufferType,
    BufferUsage,
    OpenGLError,
    Program,
    Shader,
    ShaderType,
    VertexArray,
)

vertext_shader_source = """#version 300 es

precision highp float;

in vec4 position;

void main()
{
   gl_Position = position;
}
"""
FRAGMENT_SHADER_TEMPLATE = """#version 300 es

precision highp float;

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

    def initialize_vbo(self, data):
        data_bytes = bytes(array.array("f", data))
        self.vbo = Buffer(BufferType.array, BufferUsage.static_draw)
        self.vbo.create()
        with self.vbo:
            self.vbo.set_data(data_bytes)

    def initialize_program(self, vertex_shader_code, fragment_shader_code):
        self.program = Program(
            [
                Shader(ShaderType.vertex, vertex_shader_code),
                Shader(ShaderType.fragment, fragment_shader_code),
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
                GL.glVertexAttribPointer(0, 4, GL.GL_FLOAT, False, 0, 0)

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
            vertex_positions = [
                1.0,  # triangle 1
                1.0,
                0.0,
                1.0,
                1.0,
                -1.0,
                0.0,
                1.0,
                -1.0,
                -1.0,
                0.0,
                1.0,
                1.0,  # triangle 2
                1.0,
                0.0,
                1.0,
                -1.0,
                -1.0,
                0.0,
                1.0,
                -1.0,
                1.0,
                0.0,
                1.0,
            ]
            self.initialize_vbo(vertex_positions)
            self.update_program()
        except OpenGLError as exc:
            self.message = exc.args[0]
            raise
        except Exception:
            self.message = traceback.format_exc()
            raise
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
            if pointer and 0 <= pointer[0] < size[0] and 0 <= pointer[1] < size[1]:
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
            elif pointer is None:
                pointer = (0, 0)
                self.drag_start = (0, 0)

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
