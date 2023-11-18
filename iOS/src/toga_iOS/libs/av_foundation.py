##########################################################################
# System/Library/Frameworks/AVFoundation.framework
##########################################################################
from ctypes import c_uint32, cdll, util

######################################################################
av_foundation = cdll.LoadLibrary(util.find_library("AVFoundation"))
######################################################################

SystemSoundID = c_uint32

av_foundation.AudioServicesPlayAlertSound.restype = None
av_foundation.AudioServicesPlayAlertSound.argtypes = [SystemSoundID]
