from utils import GUI

if GUI == 'pyside2':
    from PySide2.QtWidgets import *

else:
    from PySide.QtGui import *
    from PySide.QtCore import QRect

    def _QWidget_grab(self, rect=QRect(0, 0, -1, -1)):
        if not rect.isValid():
            return QPixmap.grabWidget(self)
        else:
            return QPixmap.grabWidget(self, rect)

    QWidget.grab = _QWidget_grab
