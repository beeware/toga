from ctypes import windll, wintypes, HRESULT, POINTER

GetScaleFactorForMonitor = windll.shcore.GetScaleFactorForMonitor
GetScaleFactorForMonitor.restype = HRESULT
GetScaleFactorForMonitor.argtypes = [wintypes.HMONITOR, POINTER(wintypes.UINT)]
