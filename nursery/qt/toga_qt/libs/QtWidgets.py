from utils import GUI

if GUI == 'pyqt5':
    from PyQt5.QtWidgets import *
    # TODO: fix QGraphicsItem if needed

else:
    from PySide2.QtWidgets import *
