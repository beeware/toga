import toga


class OpenGLApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(
            size=(800, 500), resizable=True, minimizable=False
        )

        opengl_view = toga.OpenGLView(self.callback_render, flex=1)

        #  Create the outer box with 2 rows
        outer_box = toga.Box(children=[opengl_view])

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()

    def callback_render(self, widget, context, **kwargs):
        context.clear_color(1.0, 0.0, 0.0, 1.0)
        context.clear(context.COLOR_BUFFER_BIT)


def main():
    return OpenGLApp("OpenGL", "org.beeware.toga.examples.opengl")


if __name__ == "__main__":
    main().main_loop()
