from platform import ios_ver

from .foundation import NSBundle

supports_liquid_glass = (
    not bool(
        NSBundle.mainBundle.objectForInfoDictionaryKey("UIDesignRequiresCompatibility")
    )
    and int(ios_ver().release.split(".")[0]) >= 26
)

__all__ = ["supports_liquid_glass"]
