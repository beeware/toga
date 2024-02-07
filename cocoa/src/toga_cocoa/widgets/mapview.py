from travertino.size import at_least

from ..libs import (
    CLLocationCoordinate2D,
    MKCoordinateRegion,
    MKCoordinateSpan,
    MKMapView,
    MKPointAnnotation,
)
from .base import Widget


class MapView(Widget):
    def create(self):
        self.native = MKMapView.alloc().init()

        # Add the layout constraints
        self.add_constraints()

    def get_location(self):
        location = self.native.centerCoordinate
        return (location.latitude, location.longitude)

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
        self.native.addAnnotation(annotation)

    def remove_pin(self, pin):
        self.native.removeAnnotation(pin._native)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
