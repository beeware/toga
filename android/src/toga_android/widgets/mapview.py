from android.preference import PreferenceManager
from org.osmdroid.config import Configuration
from org.osmdroid.tileprovider.tilesource import TileSourceFactory
from org.osmdroid.util import GeoPoint
from org.osmdroid.views import MapView as OSMMapView
from org.osmdroid.views.overlay import Marker

from .base import Widget


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
        marker.setImage(None)
        marker.setPosition(GeoPoint(*pin.location))
        marker.setTitle(pin.title)

        pin._native = marker

        self.native.getOverlays().add(marker)

    def update_pin(self, pin):
        pin._native.setPosition(GeoPoint(*pin.location))
        pin._native.setTitle(pin.title)

        # This is a hack to force a refresh of the display
        self.native.getController().setCenter(self.native.getMapCenter())

    def remove_pin(self, pin):
        self.native.getOverlays().remove(pin._native)
        pin._native = None

        # This is a hack to force a refresh of the display
        self.native.getController().setCenter(self.native.getMapCenter())
