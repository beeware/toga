import travertino

__version__ = travertino._package_version(__file__, __name__)

ENABLE_LIQUID_GLASS_ADAPTATION = False
"""
Some styling features called "Liquid Glass" on macOS are only
enabled if the binary is compiled with an SDK version of 26+.
The SDK version can be difficult to detect; therefore, set
this flag to True if the main binary of the application that
uses Toga, most of the time the Briefcase app template, is
compiled with macOS 26+ and does not contain ``UIDesignRequiresCompatibility``.
macOS 18- will continue to disable adaptations that Toga makes
to accommodate Liquid Glass.

This property should be set before any Toga objects are created
or configured.
"""
