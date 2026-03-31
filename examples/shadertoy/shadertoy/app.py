import asyncio

import toga
import toga.sources
from toga.constants import COLUMN, MONOSPACE

SOURCE = """
// Replace this with shaders from shadertoy.com
// This is a simple example, so it doesn't handle channel, video or sound.
//
// Good examples to try:
// - Protean Clouds: https://www.shadertoy.com/view/3l23Rh
// - Star Nest: https://www.shadertoy.com/view/XlfGRj
// - Cyber Fuji 2020: https://www.shadertoy.com/view/Wt33Wf
// - Neural Stanford Bunny: https://www.shadertoy.com/view/wtVyWK
// - Seascape: https://www.shadertoy.com/view/Ms2SD1
// - Flame: https://www.shadertoy.com/view/MdX3zr
// - Input - Mouse - https://www.shadertoy.com/view/Mss3zH


void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord/iResolution.xy;

    // Time varying pixel color
    vec3 col = 0.5 + 0.5*cos(iTime+uv.xyx+vec3(0,2,4));

    // Output to screen
    fragColor = vec4(col,1.0);
}
"""


class ShadertoyApp(toga.App):
    def startup(self):
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

        if toga.backend in {"toga_cocoa", "toga_qt", "toga_gtk"}:
            from .renderer_pyopengl import Renderer
        else:
            raise RuntimeError(f"Toga backend {toga.backend} is not supported.")

        self.renderer = Renderer(SOURCE)

        opengl_view = toga.OpenGLView(self.renderer, width=640, height=360)

        async def animate():
            while True:
                self.message.text = self.renderer.message
                await asyncio.sleep(0.005)
                opengl_view.redraw()

        loop = asyncio.get_running_loop()
        loop.create_task(animate())

        #  Create the outer box with 2 rows
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
        self.renderer.set_source(widget.value)


def main():
    return ShadertoyApp("Shadertoy Example", "org.beeware.toga.examples.shadertoy")


if __name__ == "__main__":
    main().main_loop()
