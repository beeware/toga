try:  # try import PyQt5
    from PyQt5.QtCore import QT_VERSION, QT_VERSION_STR
    GUI = 'pyqt5'

except ImportError:
    try:  # try import PySide2
        from PySide2.QtCore import qVersion

        GUI = 'pyside2'
        _major, _minor, _micro = tuple(map(int, qVersion().split(".")[:3]))
        QT_VERSION = (_major << 16) + (
            _minor << 8) + _micro  # fix version for pyside2
        QT_VERSION_STR = '{}.{}.{}'.format(
            _major, _minor, _micro)  # fix version string for pyside2

    except ImportError:
        raise

# TODO: add imports for PyQt4 and PySide with patches.
