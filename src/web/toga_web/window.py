# from travertino.layout import Viewport

# from toga.command import GROUP_BREAK, SECTION_BREAK
# from toga.handlers import wrapped_handler

from . import dialogs


class WebViewport:
    def __init__(self):
        self.dpi = 96
        self.baseline_dpi = 96

    @property
    def width(self):
        return 1024

    @property
    def height(self):
        return 768


class Window:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        pass

    def __html__(self):
        return """
            <main id="toga_{id}" class="container" role="main">
            {content}
            </main>
        """.format(
            id=self.interface.id,
            content=self.interface.content._impl.__html__()
        )

    def set_title(self, title):
        self.interface.factory.not_implemented('Window.set_title()')

    def set_app(self, app):
        self.interface.factory.not_implemented('Window.set_app()')

    def create_toolbar(self):
        self.interface.factory.not_implemented('Window.create_toolbar()')

    def set_content(self, widget):
        self.interface.factory.not_implemented('Window.set_content()')
        widget.viewport = WebViewport()
        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

    def show(self):
        self.interface.factory.not_implemented('Window.show()')
        # self.native.show_all()

        # # Now that the content is visible, we can do our initial hinting,
        # # and use that as the basis for setting the minimum window size.
        # self.interface.content._impl.rehint()
        # self.interface.content.style.layout(self.interface.content, Viewport(0, 0))
        # self.interface.content._impl.min_width = self.interface.content.layout.width
        # self.interface.content._impl.min_height = self.interface.content.layout.height

    def on_close(self, *args):
        pass

    def on_size_allocate(self, widget, allocation):
        pass

    def close(self):
        self.interface.factory.not_implemented('Window.close()')

    def set_position(self, position):
        self.interface.factory.not_implemented('Window.set_position()')

    def set_size(self, size):
        self.interface.factory.not_implemented('Window.set_size()')

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented('Window.set_full_screen()')

    def info_dialog(self, title, message):
        return dialogs.info(self.interface, title, message)

    def question_dialog(self, title, message):
        return dialogs.question(self.interface, title, message)

    def confirm_dialog(self, title, message):
        return dialogs.confirm(self.interface, title, message)

    def error_dialog(self, title, message):
        return dialogs.error(self.interface, title, message)

    def stack_trace_dialog(self, title, message, content, retry=False):
        return dialogs.stack_trace(self.interface, title, message, content, retry)

    def save_file_dialog(self, title, suggested_filename, file_types):
        return dialogs.save_file(self.interface, title, suggested_filename, file_types)

    def open_file_dialog(self, title, initial_directory, file_types, multiselect):
        return dialogs.open_file(self.interface, title, file_types, multiselect)

    def select_folder_dialog(self, title, initial_directory, multiselect):
        return dialogs.select_folder(self.interface, title, multiselect)
