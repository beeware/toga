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
# AVAnimation.h

AVLayerVideoGravityResizeAspectFill = objc_const(
    av_foundation, "AVLayerVideoGravityResizeAspectFill"
)

######################################################################
# AVCaptureDevice.h
AVCaptureDevice = ObjCClass("AVCaptureDevice")


class AVAuthorizationStatus(Enum):
    NotDetermined = 0
    Restricted = 1
    Denied = 2
    Authorized = 3


######################################################################
# AVCaptureDeviceInput.h
AVCaptureDeviceInput = ObjCClass("AVCaptureDeviceInput")

######################################################################
# AVCaptureMetadataOutput.h
AVCaptureMetadataOutput = ObjCClass("AVCaptureMetadataOutput")

######################################################################
# AVMetadataObject.h
AVMetadataMachineReadableCodeObject = ObjCClass("AVMetadataMachineReadableCodeObject")

######################################################################
# AVMetadataObjectType constants
AVMetadataObjectTypeQRCode = objc_const(av_foundation, "AVMetadataObjectTypeQRCode")
AVMetadataObjectTypeCode128Code = objc_const(
    av_foundation, "AVMetadataObjectTypeCode128Code"
)
AVMetadataObjectTypeEAN13Code = objc_const(
    av_foundation, "AVMetadataObjectTypeEAN13Code"
)
AVMetadataObjectTypeEAN8Code = objc_const(av_foundation, "AVMetadataObjectTypeEAN8Code")
AVMetadataObjectTypePDF417Code = objc_const(
    av_foundation, "AVMetadataObjectTypePDF417Code"
)
AVMetadataObjectTypeAztecCode = objc_const(
    av_foundation, "AVMetadataObjectTypeAztecCode"
)
AVMetadataObjectTypeDataMatrixCode = objc_const(
    av_foundation, "AVMetadataObjectTypeDataMatrixCode"
)

######################################################################
# AVMediaFormat.h
AVMediaTypeAudio = objc_const(av_foundation, "AVMediaTypeAudio")
AVMediaTypeVideo = objc_const(av_foundation, "AVMediaTypeVideo")

######################################################################
# AVCaptureSession.h
AVCaptureSession = ObjCClass("AVCaptureSession")

######################################################################
# AVCaptureVideoPreviewLayer.h
AVCaptureVideoPreviewLayer = ObjCClass("AVCaptureVideoPreviewLayer")
