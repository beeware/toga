from utils import GUI

if GUI == 'pyqt5':
    from PyQt5.QtGui import *
    # TODO: fix QWheelEvent if needed

else:
    from PySide2.QtGui import *
