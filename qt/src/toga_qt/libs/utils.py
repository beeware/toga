from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from travertino.constants import BOTTOM, CENTER, JUSTIFY, LEFT, RIGHT, TOP


def qt_text_align(valuex, valuey):
    return {
        LEFT: Qt.AlignLeft,
        CENTER: Qt.AlignHCenter,
        RIGHT: Qt.AlignRight,
        JUSTIFY: Qt.AlignJustify,
    }[valuex] | {
        TOP: Qt.AlignTop,
        CENTER: Qt.AlignVCenter,
        BOTTOM: Qt.AlignBottom,
    }[valuey]


def create_qapplication():
    return QApplication.instance() or QApplication()
