##########################################################################
# System/Library/Frameworks/CoreLocation.framework
##########################################################################
from ctypes import Structure, c_double
from enum import Enum

from rubicon.objc import ObjCClass
from rubicon.objc.runtime import load_library
from rubicon.objc.types import with_preferred_encoding

######################################################################
core_location = load_library("CoreLocation")
######################################################################

######################################################################
# CLLocation.h

CLLocationDegrees = c_double


@with_preferred_encoding(b"{CLLocationCoordinate2D=dd}")
class CLLocationCoordinate2D(Structure):
    _fields_ = [
        ("latitude", CLLocationDegrees),
        ("longitude", CLLocationDegrees),
    ]

    def __repr__(self):
        return f"<CLLocationCoordinate2D({self.latitude:.4f}, {self.longitude:.4f})>"

    def __str__(self):
        return f"({self.latitude:.4f}, {self.longitude:.4f})"


######################################################################
# CLLocationManager.h
CLLocationManager = ObjCClass("CLLocationManager")


class CLAuthorizationStatus(Enum):
    NotDetermined = 0
    Restricted = 1
    Denied = 2
    AuthorizedAlways = 3
    AuthorizedWhenInUse = 4
