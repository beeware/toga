from utils import GUI, QT_VERSION, QT_VERSION_STR

if GUI == 'pyside2':
    from PySide2.QtCore import *

else:
    from PySide.QtCore import *
