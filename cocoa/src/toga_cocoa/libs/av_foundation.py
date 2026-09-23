##########################################################################
# System/Library/Frameworks/AVFoundation.framework
##########################################################################
from ctypes import cdll, util
from enum import Enum

from rubicon.objc import ObjCClass, objc_const

######################################################################
av_foundation = cdll.LoadLibrary(util.find_library("AVFoundation"))
######################################################################

######################################################################
# AVAnimation.h

AVLayerVideoGravityResize = objc_const(av_foundation, "AVLayerVideoGravityResize")
AVLayerVideoGravityResizeAspect = objc_const(
    av_foundation, "AVLayerVideoGravityResizeAspect"
)
AVLayerVideoGravityResizeAspectFill = objc_const(
    av_foundation, "AVLayerVideoGravityResizeAspectFill"
)

######################################################################
# AVMediaFormat.h

AVMediaTypeAudio = objc_const(av_foundation, "AVMediaTypeAudio")
AVMediaTypeVideo = objc_const(av_foundation, "AVMediaTypeVideo")

######################################################################
# AVCaptureSessionPreset.h

AVCaptureSessionPresetPhoto = objc_const(av_foundation, "AVCaptureSessionPresetPhoto")

######################################################################
# AVCaptureDevice.h

AVCaptureDevice = ObjCClass("AVCaptureDevice")


class AVAuthorizationStatus(Enum):
    NotDetermined = 0
    Restricted = 1
    Denied = 2
    Authorized = 3


class AVCaptureFlashMode(Enum):
    Off = 0
    On = 1
    Auto = 2


######################################################################
# AVCaptureDeviceInput.h
AVCaptureDeviceInput = ObjCClass("AVCaptureDeviceInput")

######################################################################
# AVCapturePhotoOutput.h

AVCapturePhotoOutput = ObjCClass("AVCapturePhotoOutput")
AVCapturePhotoSettings = ObjCClass("AVCapturePhotoSettings")

######################################################################
# AVCaptureSession.h

AVCaptureSession = ObjCClass("AVCaptureSession")

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
# AVCaptureVideoPreviewLayer.h

AVCaptureVideoPreviewLayer = ObjCClass("AVCaptureVideoPreviewLayer")
