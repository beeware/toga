from . import dialogs

from rubicon.java import JavaClass, JavaInterface
Intent = JavaClass("android/content/Intent")
Activity = JavaClass("android/app/Activity")
Uri = JavaClass("android/net/Uri")

class AndroidViewport:
    def __init__(self, native):
        self.native = native
        self.dpi = self.native.getContext().getResources().getDisplayMetrics().densityDpi
        # Toga needs to know how the current DPI compares to the platform default,
        # which is 160: https://developer.android.com/training/multiscreen/screendensities
        self.baseline_dpi = 160

    @property
    def width(self):
        return self.native.getContext().getResources().getDisplayMetrics().widthPixels

    @property
    def height(self):
        return self.native.getContext().getResources().getDisplayMetrics().heightPixels


class Window:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        pass

    def set_app(self, app):
        self.app = app

    def set_content(self, widget):
        # Set the widget's viewport to be based on the window's content.
        widget.viewport = AndroidViewport(widget.native)
        # Set the app's entire contentView to the desired widget. This means that
        # calling Window.set_content() on any Window object automatically updates
        # the app, meaning that every Window object acts as the MainWindow.
        self.app.native.setContentView(widget.native)

        # Attach child widgets to widget as their container.
        for child in widget.interface.children:
            child._impl.container = widget
            child._impl.viewport = widget.viewport

    def set_title(self, title):
        pass

    def set_position(self, position):
        pass

    def set_size(self, size):
        pass

    def create_toolbar(self):
        pass

    def show(self):
        pass

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented('Window.set_full_screen()')

    def info_dialog(self, title, message):
        dialogs.info(self, title, message)

    def question_dialog(self, title, message):
        self.interface.factory.not_implemented('Window.question_dialog()')

    def confirm_dialog(self, title, message):
        self.interface.factory.not_implemented('Window.confirm_dialog()')

    def error_dialog(self, title, message):
        self.interface.factory.not_implemented('Window.error_dialog()')

    def stack_trace_dialog(self, title, message, content, retry=False):
        self.interface.factory.not_implemented('Window.stack_trace_dialog()')

    def save_file_dialog(self, title, suggested_filename, file_types):
        self.interface.factory.not_implemented('Window.save_file_dialog()')

    async def open_file_dialog(self, title, initial_uri, file_mime_types, multiselect):
        """
        Opens a file chooser dialog and returns the chosen file as content URI.
        Raises a ValueError when nothing has been selected

        :param str title: The title is ignored on Android
        :param initial_uri: The initial location shown in the file chooser. Must be a content URI, e.g.
                            'content://com.android.externalstorage.documents/document/primary%3ADownload%2FTest-dir'
        :type initial_uri: str or None
        :param file_mime_types: The file types allowed to select. Must be MIME types, e.g. ['application/pdf'].
                                Currently ignored to avoid error in rubicon
        :type file_mime_types: list[str] or None
        :param bool multiselect: If True, then several files can be selected
        :returns: The content URI of the chosen file or a list of content URIs when multiselect=True.
        :rtype: str or list[str]
        """
        print('Invoking Intent ACTION_OPEN_DOCUMENT')
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType("*/*")
        if initial_uri is not None and initial_uri != '':
            intent.putExtra("android.provider.extra.INITIAL_URI", Uri.parse(initial_uri))
        if file_mime_types is not None and file_mime_types != ['']:
            # intent.putExtra(Intent.EXTRA_MIME_TYPES, file_mime_types)  # currently creates an error in rubicon
            pass
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, multiselect)
        selected_uri = None
        result = await self.app.invoke_intent_for_result(intent)
        if result["resultCode"] == Activity.RESULT_OK:
            if result["resultData"] is not None:
                selected_uri = result["resultData"].getData()
                if multiselect is True:
                    if selected_uri is None:
                        selected_uri = []
                        clip_data = result["resultData"].getClipData()
                        if clip_data is not None:
                            for i in range (0, clip_data.getItemCount()):
                                selected_uri.append(str(clip_data.getItemAt(i).getUri()))
                    else:
                        selected_uri = [str(selected_uri)]
        if selected_uri is None:
            raise ValueError("No filename provided in the open file dialog")
        return selected_uri
