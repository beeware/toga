import uuid
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtQuickWidgets import QQuickWidget
from travertino.size import at_least

import toga
from toga.types import LatLng

from .base import Widget


class MapBridge(QObject):
    pinClickedSignal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(str)
    def pinClicked(self, uid):
        self.pinClickedSignal.emit(uid)


class MapView(Widget):
    def create(self):
        self._qml_path = str(Path(__file__).parent.parent / "resources/mapview.qml")

        self.native = QQuickWidget()
        self.native.setResizeMode(QQuickWidget.SizeRootObjectToView)

        self._ready = False

        # Bridge
        self.bridge = MapBridge()
        self.native.rootContext().setContextProperty("bridge", self.bridge)
        self.native.rootContext().setContextProperty(
            "cachePath", str(toga.App.app.paths.cache / "QtLocation")
        )

        # Connect the bridge signals
        self.bridge.pinClickedSignal.connect(self._on_pin_clicked)

        # Load QML
        self.native.setSource(self._qml_path)

        # Reverse lookup of pins
        self.pins = {}

    def _unmarshall_latlng(self, value):
        nums = tuple(float(v) for v in value[7:-1].split(","))
        value = LatLng(*nums)
        return value

    # --------------------------
    # Public API
    # --------------------------
    def add_pin(self, pin):
        if not hasattr(pin, "uid") or not pin.uid:
            pin.uid = str(uuid.uuid4())

        self.native.rootObject().addPin(
            pin.uid, pin.location[0], pin.location[1], pin.title, pin.subtitle
        )
        self.pins[pin.uid] = pin

    def update_pin(self, pin):
        self.native.rootObject().updatePin(
            pin.uid, pin.location[0], pin.location[1], pin.title, pin.subtitle
        )

    def remove_pin(self, pin):
        self.native.rootObject().removePin(pin.uid)
        del self.pins[pin.uid]

    def set_location(self, position):
        lat, lon = position
        self.native.rootObject().setCenter(lat, lon)

    def get_location(self):
        return self._unmarshall_latlng(self.native.rootObject().getCenter())

    def set_zoom(self, zoom):
        self.native.rootObject().setZoom(zoom)

    def get_zoom(self):
        return self.native.rootObject().getZoom()

    def _on_pin_clicked(self, uid):
        pin = self.pins.get(uid)
        self.interface.on_select(pin=pin)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
