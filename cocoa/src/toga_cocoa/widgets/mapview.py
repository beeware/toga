import math

from rubicon.objc import objc_method, objc_property
from travertino.size import at_least

from toga.types import LatLng

from ..libs import (
    CLLocationCoordinate2D,
    MKCoordinateRegion,
    MKCoordinateSpan,
    MKMapView,
    MKPointAnnotation,
)
from .base import Widget


class TogaMapView(MKMapView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def mapView_didSelectAnnotationView_(self, mapView, view) -> None:
        pin = self.impl.pins[view.annotation]
        self.interface.on_select(pin=pin)

    @objc_method
    def mapView_regionDidChangeAnimated_(self, mapView, animated: bool) -> None:
        # Once an animation finishes, we know the future location has been reached.
        self.impl.future_location = None


class MapView(Widget):
    def create(self):
        self.native = TogaMapView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.zoomEnabled = True
        self.native.scrollEnabled = True

        # Setting the zoom level requires knowing the center of the map; but if you set
        # the zoom immediately after changing the location, the map may not have
        # finished animating to the new location yet. Whenever we change location, store
        # the desired future location, so that any zoom changes that occur during
        # animation can use the desired *future* location as the center of the zoom
        # window, rather than wherever the window is mid-pan.
        self.future_location = None

        # Setting the zoom level also requires knowing the size of the rendered area.
        # We won't know this until layout happens at least once, so retain a backlog
        # of requests for location and zoom until layout has occurred.
        self.backlog = {}

        # Reverse lookup of map annotations to pins
        self.pins = {}

        # Only set the delegate once the properties on the impl are in place to support
        # any events that might occur. We use a standalone delegate class because
        # MKMapView seems to have issues being subclassed (and subclassing is explicitly
        # called out in the docs.)
        self.native.delegate = self.native

        # Add the layout constraints
        self.add_constraints()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        if self.backlog is not None:
            # This is the first layout pass; we now know the size of the window, so we
            # can process outstanding requests. Basic widget construction should
            # *always* set location and zoom, so the keys *should* always exist; the
            # exception is caught as a safety catch.
            backlog = self.backlog
            self.backlog = None
            try:
                self.set_location(backlog["location"])
            except KeyError:  # pragma: no cover
                pass
            try:
                self.set_zoom(backlog["zoom"])
            except KeyError:  # pragma: no cover
                pass

    def get_location(self):
        location = self.native.centerCoordinate
        return LatLng(location.latitude, location.longitude)

    def set_location(self, position):
        if self.backlog is None:
            self.future_location = CLLocationCoordinate2D(*position)
            self.native.setCenterCoordinate(
                self.future_location,
                animated=True,
            )
        else:
            self.backlog["location"] = position

    def get_zoom(self):
        # Reverse engineer zoom level based on a 256 pixel square.
        # See set_zoom for the rationale behind the math.
        return math.log2(
            (360 * self.interface.layout.height)
            / (self.native.region.span.latitudeDelta * 256)
        )

    def set_zoom(self, zoom):
        if self.backlog is None:
            # The zoom level indicates how many degrees of latitude will be displayed in a
            # 256 pixel vertical range. Determine how many degrees of latitude that is,
            # and scale to the size of the visible vertical space.

            # The vertical axis can't show more than 180 degrees of latitude, so clip
            # the range to that value. The OSM zoom level is based on 360 degrees of
            # latitude being split into 2**zoom sections.
            delta = min(
                180.0,
                (360 * self.interface.layout.height) / (256 * 2**zoom),
            )
            # If we're currently panning to a new location, use the desired *future*
            # location as the center of the zoom region. Otherwise use the current center
            # coordinate.
            center = (
                self.future_location
                if self.future_location is not None
                else self.native.centerCoordinate
            )
            region = MKCoordinateRegion(
                center,
                MKCoordinateSpan(delta, 0),
            )
            self.native.setRegion(region, animated=True)
        else:
            self.backlog["zoom"] = zoom

    def add_pin(self, pin):
        annotation = MKPointAnnotation.alloc().initWithCoordinate(
            CLLocationCoordinate2D(*pin.location),
            title=pin.title,
            subtitle=pin.subtitle,
        )
        pin._native = annotation
        self.pins[annotation] = pin

        self.native.addAnnotation(annotation)

    def update_pin(self, pin):
        pin._native.coordinate = CLLocationCoordinate2D(*pin.location)
        pin._native.title = pin.title
        pin._native.subtitle = pin.subtitle

    def remove_pin(self, pin):
        self.native.removeAnnotation(pin._native)
        del self.pins[pin._native]
        pin._native = None

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
