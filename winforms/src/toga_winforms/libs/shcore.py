from ctypes import HRESULT, POINTER, windll, wintypes

GetScaleFactorForMonitor = windll.shcore.GetScaleFactorForMonitor
GetScaleFactorForMonitor.restype = HRESULT
GetScaleFactorForMonitor.argtypes = [wintypes.HMONITOR, POINTER(wintypes.UINT)]
