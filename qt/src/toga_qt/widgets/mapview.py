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

        self._backlog = []
        self._ready = False

        # Bridge
        self.bridge = MapBridge()
        self.native.rootContext().setContextProperty("bridge", self.bridge)
        self.native.rootContext().setContextProperty(
            "cachePath", str(toga.App.app.paths.cache / "QtLocation")
        )

        # Connect the bridge signals
        self.bridge.pinClickedSignal.connect(self._on_pin_clicked)

        # Flush backlog when QQuickWidget is ready
        self.native.statusChanged.connect(self._on_status_changed)

        # Load QML
        self.native.setSource(self._qml_path)

        # Reverse lookup of pins
        self.pins = {}

    def _on_status_changed(self, status):
        if status == QQuickWidget.Ready:
            self._flush_backlog()

    def _flush_backlog(self):
        self._ready = True
        for func, args, kwargs in self._backlog:
            func(*args, **kwargs)
        self._backlog = []

    def _unmarshall(self, value):
        if value is None:
            return None
        elif isinstance(value, float):
            return value
        elif value.startswith("LatLng("):
            nums = tuple(float(v) for v in value[7:-1].split(","))
            value = LatLng(*nums)
        elif value.startswith("Array[,"):
            value = value[7:-1].split(",")
        return value

    def _invoke(self, func, *args, **kwargs):
        if self._ready:
            return func(*args, **kwargs)
        else:
            self._backlog.append((func, args, kwargs))
            return None

    # --------------------------
    # Public API
    # --------------------------
    def add_pin(self, pin):
        if not hasattr(pin, "uid") or not pin.uid:
            pin.uid = str(uuid.uuid4())

        def _add():
            self.native.rootObject().addPin(
                pin.uid, pin.location[0], pin.location[1], pin.title, pin.subtitle
            )
            self.pins[pin.uid] = pin

        return self._invoke(_add)

    def update_pin(self, pin):
        def _update():
            self.native.rootObject().updatePin(
                pin.uid, pin.location[0], pin.location[1], pin.title, pin.subtitle
            )

        return self._invoke(_update)

    def remove_pin(self, pin):
        def _remove():
            self.native.rootObject().removePin(pin.uid)
            if pin.uid in self.pins:
                del self.pins[pin.uid]

        return self._invoke(_remove)

    def list_pins(self):
        root = self.native.rootObject()
        if root:
            return [self.pins[uid] for uid in self._unmarshall(root.listPins())]
        else:
            return []

    def set_location(self, position):
        lat, lon = position
        return self._invoke(lambda: self.native.rootObject().setCenter(lat, lon))

    def get_location(self):
        root = self.native.rootObject()
        if root:
            return self._unmarshall(root.getCenter())
        else:
            return LatLng(0, 0)

    def set_zoom(self, zoom):
        return self._invoke(lambda: self.native.rootObject().setZoom(zoom))

    def get_zoom(self):
        root = self.native.rootObject()
        if root:
            return self._unmarshall(root.getZoom())
        else:
            return 10

    def _on_pin_clicked(self, uid):
        pin = self.pins.get(uid)
        self.interface.on_select(pin)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
