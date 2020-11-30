from utils import GUI, QT_VERSION, QT_VERSION_STR

if GUI == 'pyqt5':
    from PyQt5.QtCore import *

else:
    from PySide2.QtCore import *
