from .foundation import NSBundle

supports_liquid_glass = bool(
    NSBundle.mainBundle().objectForInfoDictionaryKey("UIDesignRequiresCompatibility")
)
__all__ = ["supports_liquid_glass"]
