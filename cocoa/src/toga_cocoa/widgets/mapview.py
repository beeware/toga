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

        # Reverse lookup of map annotations to pins
        self.pins = {}

        # Only set the delegate once the properties on the impl are in place to support
        # any events that might occur. We use a standalone delegate class because
        # MKMapView seems to have issues being subclassed (and subclassing is explicitly
        # called out in the docs.)
        self.native.delegate = self.native

        # Add the layout constraints
        self.add_constraints()

    def get_location(self):
        location = self.native.centerCoordinate
        return LatLng(location.latitude, location.longitude)

    def set_location(self, position):
        self.future_location = CLLocationCoordinate2D(*position)
        self.native.setCenterCoordinate(
            self.future_location,
            animated=True,
        )

    def set_zoom(self, zoom):
        # MKMapView uses a delta of latitude/longitude as the indicator of zoom extent.
        delta = {
            0: 30,  # Whole country.
            1: 5,  # See a city in relation to nearby cities.
            2: 0.5,  # The extents of a large city
            3: 0.05,  # Suburb/locality level.
            4: 0.005,  # Multiple city blocks
            5: 0.002,  # City block
        }[zoom]

        # If we're currently panning to a new location, use the desired *future*
        # location as the center of the zoom region. Otherwise use the current center
        # coordinate.
        region = MKCoordinateRegion(
            (
                self.future_location
                if self.future_location is not None
                else self.native.centerCoordinate
            ),
            MKCoordinateSpan(delta, delta),
        )
        self.native.setRegion(region, animated=True)

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
