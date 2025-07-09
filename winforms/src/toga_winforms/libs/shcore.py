from ctypes import HRESULT, POINTER, windll, wintypes

try:
	shcore = windll.shcore
except FileNotFoundError:
	# Windows <8.1
	shcore = None

if shcore:
	GetScaleFactorForMonitor = shcore.GetScaleFactorForMonitor
	GetScaleFactorForMonitor.restype = HRESULT
	GetScaleFactorForMonitor.argtypes = [wintypes.HMONITOR, POINTER(wintypes.UINT)]
else:
	GetScaleFactorForMonitor = None
