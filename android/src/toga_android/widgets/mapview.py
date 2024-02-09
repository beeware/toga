from pathlib import Path

from android.graphics import BitmapFactory
from android.graphics.drawable import BitmapDrawable
from android.preference import PreferenceManager
from java import dynamic_proxy
from org.osmdroid.config import Configuration
from org.osmdroid.tileprovider.tilesource import TileSourceFactory
from org.osmdroid.util import GeoPoint
from org.osmdroid.views import MapView as OSMMapView
from org.osmdroid.views.overlay import Marker

from .base import Widget


class TogaOnMarkerClickListener(dynamic_proxy(Marker.OnMarkerClickListener)):
    def __init__(self, map_impl):
        super().__init__()
        self.map_impl = map_impl

    def onMarkerClick(self, marker, map_view):
        result = marker.onMarkerClickDefault(marker, map_view)
        pin = self.map_impl.pins[marker]
        self.map_impl.interface.on_select(pin=pin)
        return result


class MapView(Widget):
    _configured = False

    def create(self):
        if not self._configured:
            app_context = self._native_activity.getApplicationContext()
            Configuration.getInstance().load(
                app_context,
                PreferenceManager.getDefaultSharedPreferences(app_context),
            )

        self.native = OSMMapView(self._native_activity)

        self.native.setTileSource(TileSourceFactory.MAPNIK)
        self.native.setBuiltInZoomControls(True)
        self.native.setMultiTouchControls(True)
        self.native.setTilesScaledToDpi(True)

        self.pins = {}

        bitmap = BitmapFactory.decodeFile(
            str(Path(__file__).parent.parent / "resources/marker.png")
        )
        self.icon = BitmapDrawable(self.native.getContext().getResources(), bitmap)

        self.marker_click_listener = TogaOnMarkerClickListener(self)

    def get_location(self):
        location = self.native.getMapCenter()
        return (location.getLatitude(), location.getLongitude())

    def set_location(self, position):
        self.native.getController().animateTo(GeoPoint(*position))

    def set_zoom(self, zoom):
        osm_zoom = {
            0: 5,
            1: 7,
            2: 11,
            3: 15,
            4: 17,
            5: 18,
        }[zoom]

        self.native.getController().zoomTo(osm_zoom, None)

    def add_pin(self, pin):
        marker = Marker(self.native)
        marker.setPosition(GeoPoint(*pin.location))
        marker.setIcon(self.icon)
        marker.setTitle(pin.title)
        marker.setSubDescription(pin.subtitle)
        marker.setOnMarkerClickListener(self.marker_click_listener)

        pin._native = marker
        self.pins[marker] = pin

        self.native.getOverlays().add(marker)

    def update_pin(self, pin):
        pin._native.setPosition(GeoPoint(*pin.location))
        pin._native.setTitle(pin.title)
        pin._native.setSubDescription(pin.subtitle)

        # This is a hack to force a refresh of the display
        self.native.getController().setCenter(self.native.getMapCenter())

    def remove_pin(self, pin):
        self.native.getOverlays().remove(pin._native)

        del self.pins[pin._native]
        pin._native = None

        # This is a hack to force a refresh of the display
        self.native.getController().setCenter(self.native.getMapCenter())
