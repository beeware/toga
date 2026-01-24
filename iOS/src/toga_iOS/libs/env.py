import platform

from .. import ENABLE_LIQUID_GLASS_ADAPTATION

IOS_VERSION = tuple(map(int, platform.ios_ver().release.split(".")))


# This is needed since the liquid glass adaptation attribute
# can be set *after* this module is imported.
class DynamicLiquidGlassFlag:
    def __bool__(self):
        return IOS_VERSION >= (26, 0) and ENABLE_LIQUID_GLASS_ADAPTATION


SUPPORTS_LIQUID_GLASS = DynamicLiquidGlassFlag()

__all__ = [
    "SUPPORTS_LIQUID_GLASS",
    "IOS_VERSION",
]
