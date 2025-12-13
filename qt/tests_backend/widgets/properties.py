import pytest
from PySide6.QtCore import Qt

from toga.style.pack import BOTTOM, CENTER, JUSTIFY, LEFT, RIGHT, TOP


def toga_x_text_align(alignment):
    if alignment & Qt.AlignLeft:
        return LEFT
    elif alignment & Qt.AlignHCenter:
        return CENTER
    elif alignment & Qt.AlignRight:
        return RIGHT
    elif alignment & Qt.AlignJustify:
        return JUSTIFY
    else:
        pytest.fail(f"Qt alignment {alignment} cannot be interpreted as horizontal")


def toga_y_text_align(alignment):
    if alignment & Qt.AlignTop:
        return TOP
    elif alignment & Qt.AlignVCenter:
        return CENTER
    elif alignment & Qt.AlignBottom:
        return BOTTOM
    else:
        pytest.fail(f"Qt alignment {alignment} cannot be interpreted as vertical")
