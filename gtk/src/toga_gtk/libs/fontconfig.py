from ctypes import CDLL, c_char_p, c_int, c_void_p, util

libfontconfig = util.find_library("fontconfig")
if libfontconfig:
    fontconfig = CDLL(libfontconfig)

    FcConfig = c_void_p

    fontconfig.FcInit.argtypes = []
    fontconfig.FcInit.restype = c_int

    fontconfig.FcConfigGetCurrent.argtypes = []
    fontconfig.FcConfigGetCurrent.restype = FcConfig

    fontconfig.FcConfigAppFontAddFile.argtypes = [FcConfig, c_char_p]
    fontconfig.FcConfigAppFontAddFile.restypes = c_int
else:  # pragma: no cover
    fontconfig = None


class _FontConfig:
    def __init__(self):
        if fontconfig:
            fontconfig.FcInit()
            self.config = fontconfig.FcConfigGetCurrent()
        else:  # pragma: no cover
            print(
                "Unable to initialize FontConfig library. "
                "Is libfontconfig.so.1 on your LD_LIBRARY_PATH?"
            )
            self.config = None

    def add_font_file(self, path):
        if self.config is None:  # pragma: no cover
            raise RuntimeError(
                "Can't load custom fonts without a working Fontconfig library"
            )

        return fontconfig.FcConfigAppFontAddFile(self.config, str(path).encode("utf-8"))


# Instantiate and configure a singleton FontConfig instance
FontConfig = _FontConfig()
