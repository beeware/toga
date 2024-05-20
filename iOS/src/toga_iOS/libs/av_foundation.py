##########################################################################
# System/Library/Frameworks/AVFoundation.framework
##########################################################################
from ctypes import c_uint32, cdll, util
from enum import Enum

from rubicon.objc import ObjCClass, objc_const

######################################################################
av_foundation = cdll.LoadLibrary(util.find_library("AVFoundation"))
######################################################################

SystemSoundID = c_uint32

av_foundation.AudioServicesPlayAlertSound.restype = None
av_foundation.AudioServicesPlayAlertSound.argtypes = [SystemSoundID]

######################################################################
# AVCaptureDevice.h
AVCaptureDevice = ObjCClass("AVCaptureDevice")


class AVAuthorizationStatus(Enum):
    NotDetermined = 0
    Restricted = 1
    Denied = 2
    Authorized = 3


######################################################################
# AVMediaFormat.h
AVMediaTypeAudio = objc_const(av_foundation, "AVMediaTypeAudio")
AVMediaTypeVideo = objc_const(av_foundation, "AVMediaTypeVideo")
