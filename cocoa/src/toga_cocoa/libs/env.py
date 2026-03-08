import platform

from .. import ENABLE_LIQUID_GLASS_ADAPTATION

MACOS_VERSION = tuple(map(int, platform.mac_ver()[0].split(".")))


# This is needed since the liquid glass adaptation attribute
# can be set *after* this module is imported.
class DynamicLiquidGlassFlag:
    def __bool__(self):
        return MACOS_VERSION >= (26, 0) and ENABLE_LIQUID_GLASS_ADAPTATION


SUPPORTS_LIQUID_GLASS = DynamicLiquidGlassFlag()

__all__ = [
    "SUPPORTS_LIQUID_GLASS",
    "MACOS_VERSION",
]
