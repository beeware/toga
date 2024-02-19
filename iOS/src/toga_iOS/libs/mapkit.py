##########################################################################
# System/Library/Frameworks/MapKit.framework
##########################################################################

from ctypes import Structure

from rubicon.objc import ObjCClass
from rubicon.objc.runtime import load_library
from rubicon.objc.types import with_encoding, with_preferred_encoding

from .core_location import CLLocationCoordinate2D, CLLocationDegrees

######################################################################
MapKit = load_library("MapKit")
######################################################################

######################################################################
# MKGeometry.h


@with_preferred_encoding(b"{MKCoordinateSpan=dd}")
class MKCoordinateSpan(Structure):
    _fields_ = [
        ("latitudeDelta", CLLocationDegrees),
        ("longitudeDelta", CLLocationDegrees),
    ]

    def __repr__(self):
        return (
            f"<MKCoordinateSpan({self.latitudeDelta:.4f}, {self.longitudeDelta:.4f})>"
        )

    def __str__(self):
        return f"({self.latitudeDelta:.4f}, {self.longitudeDelta:.4f})"


# The preferred encoding is what the widget *should* use.
# However, [MKMapView setRegion:animated:] returns anonymous structures in the
# encoding, so we register that as an encoding as well.
@with_preferred_encoding(
    b"{MKCoordinateRegion={CLLocationCoordinate2D=dd}{MKCoordinateSpan=dd}}"
)
@with_encoding(b"{?={CLLocationCoordinate2D=dd}{?=dd}}")
class MKCoordinateRegion(Structure):
    _fields_ = [
        ("center", CLLocationCoordinate2D),
        ("span", MKCoordinateSpan),
    ]

    def __repr__(self):
        return f"<MKCoordinateRegion({self.center!r}, span={self.span!r})>"

    def __str__(self):
        return f"{self.center}, span={self.span}"


######################################################################
# MKMapView.h
MKMapView = ObjCClass("MKMapView")

######################################################################
# MKPointAnnotation.h
MKPointAnnotation = ObjCClass("MKPointAnnotation")
