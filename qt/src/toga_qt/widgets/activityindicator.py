from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtQuickWidgets import QQuickWidget

from .base import Widget

#######################################################################################
# Implementation note:
#
# Qt does not provide a Widget for an Activity Indicator; however, it does
# provide a QML type; set up a pre-initialized QML file that can be embedded
# into a Qt Widgets Application to represent the spinner.
#######################################################################################


class ActivityIndicator(Widget):
    def create(self):
        self.native = QQuickWidget()
        self.native.setSource(
            str(Path(__file__).parent.parent / "resources/activityindicator.qml")
        )
        self.native.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.running = False
        self.ai_hidden = True
        self.native.setAttribute(Qt.WA_AlwaysStackOnTop)
        self.native.setAttribute(Qt.WA_TranslucentBackground)
        self.native.setClearColor(Qt.transparent)

    def _apply_hidden(self, hidden):
        self.native.setVisible(self.running and not hidden)
        self.ai_hidden = hidden

    def is_running(self):
        return self.running

    def start(self):
        self.running = True
        self.native.setVisible(not self.ai_hidden)

    def stop(self):
        self.native.setVisible(False)
        self.running = False

    def rehint(self):
        self.interface.intrinsic.width = 32
        self.interface.intrinsic.height = 32
