import asyncio

import toga
import toga.sources

from .obj_file import parse_obj_file
from .obj_file_renderer import ObjFileRenderer


class ObjFile(toga.Document):
    description = "Wavefront Obj File"
    extensions = ["obj"]

    def create(self):
        # Create the main window for the document. The window has a single widget;
        # when that widget changes, the document is modified.
        self.renderer = ObjFileRenderer()

        opengl_view = toga.OpenGLView(self.renderer, flex=1)

        async def animate():
            while True:
                await asyncio.sleep(0.01)
                opengl_view.redraw()

        loop = asyncio.get_running_loop()
        self.task = loop.create_task(animate())

        outer_box = toga.Box(children=[opengl_view])

        self.main_window = toga.DocumentWindow(
            doc=self,
            content=outer_box,
            on_close=self.stop_animation,
        )

    def read(self):
        # Read the content of the file represented by the document, and populate the
        # widgets in the main window with that content.
        try:
            self.renderer.data = parse_obj_file(self.path)
        except Exception:
            import traceback

            traceback.print_exc()
            dialog = toga.StackTraceDialog(
                title=f"Error loading {self.path}",
                message="Exception while reading file.",
                content=traceback.format_exc(),
            )
            # hold reference while task is running
            self._dialog_task = asyncio.create_task(self.main_window.dialog(dialog))
            # remove reference when done
            self._dialog_task.add_done_callback(
                lambda task: self.__delattr__("_dialog_task")
            )
            self.main_window.close()

    def stop_animation(self, *args, **kwargs):
        self.task.cancel()
        return True


class OpenGLApp(toga.App):
    def startup(self):
        self.main_window = None
        self.documents.open(self.paths.app / "resources" / "well.obj")


def main():
    return OpenGLApp(
        "Obj File Viewer Example",
        "org.beeware.toga.examples.obj-viewer",
        document_types=[ObjFile],
    )


if __name__ == "__main__":
    main().main_loop()
