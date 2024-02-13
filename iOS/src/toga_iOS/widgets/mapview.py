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


class MapView(Widget):
    def create(self):
        self.native = TogaMapView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.delegate = self.native

        self.native.zoomEnabled = True
        self.native.scrollEnabled = True

        # Reverse lookup of map annotations to pins
        self.pins = {}

        # Add the layout constraints
        self.add_constraints()

    def get_location(self):
        location = self.native.centerCoordinate
        return LatLng(location.latitude, location.longitude)

    def set_location(self, position):
        self.native.setCenterCoordinate(
            CLLocationCoordinate2D(*position),
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

        region = MKCoordinateRegion(
            self.native.centerCoordinate,
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
