from PySide2.QtCore import qVersion

_major, _minor, _micro = tuple(map(int, qVersion().split(".")[:3]))
QT_VERSION = (_major << 16) + (
    _minor << 8) + _micro  # fix version
QT_VERSION_STR = '{}.{}.{}'.format(
    _major, _minor, _micro)  # fix version string
