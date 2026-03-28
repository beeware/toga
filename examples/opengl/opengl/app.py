import toga


class OpenGLApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(
            size=(800, 500), resizable=True, minimizable=False
        )

        if toga.backend in {"toga_cocoa", "toga_qt", "toga_gtk"}:
            from .renderer_pyopengl import Renderer
        elif toga.backend == "toga_android":
            from .renderer_android import Renderer
        elif toga.backend == "toga_iOS":
            from .renderer_iOS import Renderer
        else:
            raise RuntimeError(f"Toga backend {toga.backend} is not supported.")

        renderer = Renderer()

        opengl_view = toga.OpenGLView(renderer, flex=1)

        #  Create the outer box with 2 rows
        outer_box = toga.Box(children=[opengl_view])

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return OpenGLApp("OpenGL", "org.beeware.toga.examples.opengl")


if __name__ == "__main__":
    main().main_loop()
