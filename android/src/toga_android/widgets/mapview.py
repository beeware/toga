from pathlib import Path

from android.graphics import BitmapFactory
from android.graphics.drawable import BitmapDrawable
from android.preference import PreferenceManager
from java import dynamic_proxy

try:
    from org.osmdroid.config import Configuration
    from org.osmdroid.tileprovider.tilesource import TileSourceFactory
    from org.osmdroid.util import GeoPoint
    from org.osmdroid.views import MapView as OSMMapView
    from org.osmdroid.views.overlay import CopyrightOverlay, Marker
except ImportError:  # pragma: no cover
    # If you've got an older project that doesn't include the OSM library,
    # this import will fail. We can't validate that in CI, so it's marked no cover
    OSMMapView = None

import toga
from toga.types import LatLng

from .base import Widget

if OSMMapView is not None:  # pragma: no branch

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

    def create(self):
        if OSMMapView is None:  # pragma: no cover
            raise RuntimeError(
                "Unable to import MapView. Ensure that the OSMDroid Android "
                "system package (org.osmdroid:osmdroid-android:6.1.0) "
                "is listed in your app's dependencies."
            )

        app_context = self._native_activity.getApplicationContext()
        configuration = Configuration.getInstance()
        configuration.load(
            app_context,
            PreferenceManager.getDefaultSharedPreferences(app_context),
        )
        # Required by the terms of the OSM license.
        configuration.setUserAgentValue(toga.App.app.app_id)

        self.native = OSMMapView(self._native_activity)

        # Add a copyright overlay, required by OSM license.
        copyright_overlay = CopyrightOverlay(app_context)
        self.native.getOverlays().add(copyright_overlay)

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
        return LatLng(location.getLatitude(), location.getLongitude())

    def set_location(self, position):
        # If there are any outstanding animations, stop them, and force the view to the
        # end state.
        self.native.getController().stopAnimation(True)
        self.native.getController().animateTo(GeoPoint(*position))

    def get_zoom(self):
        return self.native.getZoomLevelDouble()

    def set_zoom(self, zoom):
        # If there are any outstanding animations, stop them, and force the view to the
        # end state.
        self.native.getController().stopAnimation(True)
        self.native.getController().zoomTo(zoom, None)

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
