import asyncio

from obj_viewer.obj_file import parse_obj_file
from obj_viewer.obj_file_renderer import ObjFileRenderer

import toga
import toga.sources


class OpenGLApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow()

        data = parse_obj_file(self.paths.app / "resources" / "well.obj")
        self.renderer = ObjFileRenderer(data)

        opengl_view = toga.OpenGLView(self.renderer, flex=1)

        async def animate():
            while True:
                await asyncio.sleep(0.01)
                opengl_view.redraw()

        loop = asyncio.get_running_loop()
        self.task = loop.create_task(animate())

        outer_box = toga.Box(children=[opengl_view])

        self.main_window.content = outer_box
        self.main_window.on_close = self.stop_animation

        # Show the main window
        self.main_window.show()

    def stop_animation(self, *args, **kwargs):
        self.task.cancel()
        return True


def main():
    return OpenGLApp(
        "Obj File Viewer Example",
        "org.beeware.toga.examples.obj-viewer-mobile",
    )


if __name__ == "__main__":
    main().main_loop()
