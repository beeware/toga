try:
    import PySide2.QtGui as QtGui
    import PySide2.QtCore as QtCore
    import PySide2.QtWidgets as QtWidgets
    lib = "pyside2"

except ImportError:
    import PyQt5.QtGui as QtGui
    import PyQt5.QtCore as QtCore
    import PyQt5.QtWidgets as QtWidgets
    lib = "pyqt5"

# TODO: import PySide and PyQt4 (need polyfills)
