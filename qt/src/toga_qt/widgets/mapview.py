import uuid
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtPositioning import QGeoCoordinate
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
        self.bridge = MapBridge()
        self.native.rootContext().setContextProperty("bridge", self.bridge)
        self.native.rootContext().setContextProperty(
            "cachePath", str(toga.App.app.paths.cache / "QtLocation")
        )
        self.bridge.pinClickedSignal.connect(self._on_pin_clicked)
        self.native.setSource(self._qml_path)
        self.pins = {}

    def _unmarshall_latlng(self, value):
        nums = tuple(float(v) for v in value[7:-1].split(","))
        value = LatLng(*nums)
        return value

    def add_pin(self, pin):
        pin.uid = str(uuid.uuid4())
        marker_obj = self.native.rootObject().makePin()
        marker_obj.setProperty("uid", pin.uid)
        marker_obj.setProperty("title", pin.title)
        marker_obj.setProperty("subtitle", pin.subtitle or "")
        marker_obj.setProperty(
            "coordinate", QGeoCoordinate(pin.location[0], pin.location[1])
        )
        self.native.rootObject().property("mapPins").setProperty(
            pin.uid, self.native.engine().toScriptValue(marker_obj)
        )
        self.native.rootObject().attachPin(
            self.native.engine().toScriptValue(marker_obj)
        )
        self.pins[pin.uid] = pin

    def update_pin(self, pin):
        pinobj = self.native.rootObject().property("mapPins").property(pin.uid)
        pinobj.setProperty("title", pin.title)
        pinobj.setProperty("subtitle", pin.subtitle or "")
        pinobj.setProperty(
            "coordinate",
            self.native.engine().toScriptValue(
                QGeoCoordinate(pin.location[0], pin.location[1])
            ),
        )

    def remove_pin(self, pin):
        self.native.rootObject().detachPin(
            self.native.rootObject().property("mapPins").property(pin.uid)
        )
        self.native.rootObject().deleteUid(pin.uid)

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
        self.interface.on_select(pin=self.pins[uid])

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
