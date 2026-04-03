import asyncio

import toga
from toga.constants import COLUMN, MONOSPACE

from .shadertoy_renderer import ShadertoyRenderer

# The default shadertoy mainImage fragment shader source to use.
# This should display slowly changing hues.
SOURCE = """
// Replace this with shaders from shadertoy.com
// This is a simple example, so it doesn't handle channels, video or
// sound, so not all shaders on shadertoy.com will work.
//
// Good examples to try:
// - Protean Clouds: https://www.shadertoy.com/view/3l23Rh
// - Star Nest: https://www.shadertoy.com/view/XlfGRj
// - Cyber Fuji 2020: https://www.shadertoy.com/view/Wt33Wf
// - Neural Stanford Bunny: https://www.shadertoy.com/view/wtVyWK
// - Seascape: https://www.shadertoy.com/view/Ms2SD1
// - Flame: https://www.shadertoy.com/view/MdX3zr
// - Input - Mouse - https://www.shadertoy.com/view/Mss3zH
//
// Or write your own: replace mainImage with shader code that sets
// fragColor based on fragCoord.  Uniforms provided by the renderer
// are:
//
//     iResolution: vec3 - w, h, pixel shape
//     iTime: float - seconds since start of shader
//     iTimeDelta: float - seconds since last frame
//     iFrame: float - count of frames since start of shader
//     iFrameRate: float - frames per second
//     iMouse: vec4 - (x, y, start_x, start_y)
//     iDate: vec4 - (year, month, day, seconds)
//
// See the docs on Shadertoy, particularly for the values in iMouse
// where the signs of start_x, start_y convey button state info.

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    // Set the color values for each pixel.

    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord/iResolution.xy;

    // Time varying pixel color
    vec3 col = 0.5 + 0.5 * cos(iTime + uv.xyx + vec3(0, 2, 4));

    // Output to screen
    fragColor = vec4(col, 1.0);
}
"""


class ShadertoyApp(toga.App):
    def startup(self):
        if toga.backend == "toga_android":
            self.main_window = toga.MainWindow()
        else:
            self.main_window = toga.MainWindow(
                size=(960, 800), resizable=True, minimizable=False
            )

        self.shadertoy_source = toga.MultilineTextInput(
            value=SOURCE,
            on_change=self.source_changed,
            font_family=["Noto Sans Mono", MONOSPACE],
            font_size=12,
            flex=1.0,
        )
        self.message = toga.Label("Starting...", flex=1.0)
        self.renderer = ShadertoyRenderer(SOURCE)

        opengl_view = toga.OpenGLView(self.renderer, width=640, height=360)

        async def animate():
            while True:
                self.message.text = self.renderer.message
                await asyncio.sleep(0.005)
                opengl_view.redraw()

        loop = asyncio.get_running_loop()
        loop.create_task(animate())

        if toga.backend in {"toga_android", "toga_iOS"}:
            # vertical layout
            outer_box = toga.Box(
                children=[
                    opengl_view,
                    toga.ScrollContainer(
                        content=self.message,
                    ),
                    self.shadertoy_source,
                ],
                direction=COLUMN,
                gap=4,
            )
        else:
            # Desktop layout
            outer_box = toga.Box(
                children=[
                    toga.Box(
                        children=[
                            opengl_view,
                            toga.ScrollContainer(
                                content=self.message,
                                flex=1.0,
                                height=360,
                            ),
                        ],
                        gap=4,
                    ),
                    self.shadertoy_source,
                ],
                direction=COLUMN,
                gap=4,
            )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()

    async def source_changed(self, widget, **kwargs):
        """Update the mainImage source in the renderer with the widget value."""
        self.renderer.source = widget.value


def main():
    return ShadertoyApp("Shadertoy Example", "org.beeware.toga.examples.shadertoy")


if __name__ == "__main__":
    main().main_loop()
