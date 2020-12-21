from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QListView, QAbstractItemView, QTreeView, QVBoxLayout


class Window():
    _IMPL_CLASS = QMainWindow  # or QWidget?

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self, app=None):
        if app:
            self.native = self._IMPL_CLASS(app)
        else:
            self.native = self._IMPL_CLASS()
        self.native._impl = self

        self.native.resize(self.interface.size[0], self.interface.size[1])

        # Set the window deletable/closeable.
        self.closeable = self.interface.closeable
        self.toolbar_native = None
        self.toolbar_items = None

    def create_toolbar(self):
        pass

    def set_content(self, widget):
        # Construct the top-level layout, and set the window's view to
        # the be the widget's native object.
        # Alaway avoid using deprecated widgets and methods.
        self.layout = QVBoxLayout()

        if self.toolbar_native:
            self.layout.addWidget(self.toolbar_native)
        self.layout.addWidget(widget.native)

        self.native.addLayout(self.layout)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

    def set_title(self, title):
        self.native.setWindowTitle(title)

    def set_position(self, position):
        pass

    def set_size(self, size):
        pass

    def set_app(self, app):
        pass

    def show(self):
        self.native.show()

    def close(self):
        self.native.close()

    def set_full_screen(self, is_full_screen):
        if is_full_screen:
            self.QWidget.showFullScreen()
        else:
            self.QWidget.showNormal()

    def on_close(self):
        pass

    def info_dialog(self, title, message):
        return bool(QMessageBox.information(self.native, title,
                                            message))  # always True

    def question_dialog(self, title, message):
        return QMessageBox.question(self.native, title,
                                    message) == QMessageBox.Yes

    def confirm_dialog(self, title, message):
        return QMessageBox.question(self.native, title, message, QMessageBox.Ok
                                    | QMessageBox.Cancel) == QMessageBox.Ok

    def error_dialog(self, title, message):
        return bool(QMessageBox.critical(self.native, title,
                                         message))  # always True

    def stack_trace_dialog(self, title, message, content, retry=False):
        self._action('show stack trace dialog',
                     title=title,
                     message=message,
                     content=content,
                     retry=retry)

    def save_file_dialog(self, title, suggested_filename, file_types):
        file_types = ';;'.join(
            map(lambda file_type: '{0} files (*.{0})'.format(file_type),
                file_types or []))
        return QFileDialog.getSaveFileName(self.native, title, message,
                                           suggested_filename, file_types)[0]

    def open_file_dialog(self, title, initial_directory, file_types,
                         multiselect):
        file_types = ';;'.join(
            map(lambda file_type: '{0} files (*.{0})'.format(file_type),
                file_types or []))
        func = QFileDialog.getOpenFileNames if multiselect else QFileDialog.getOpenFileName
        return func(self.native, title, message, initial_directory,
                    file_types)[0]

    def select_folder_dialog(self, title, initial_directory, multiselect):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        file_view = file_dialog.findChild(QListView, 'listView')

        # to make it possible to select multiple directories:
        if file_view:
            file_view.setSelectionMode(QAbstractItemView.MultiSelection)
        f_tree_view = file_dialog.findChild(QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(QAbstractItemView.MultiSelection)

        if file_dialog.exec():
            paths = file_dialog.selectedFiles()

        return paths
