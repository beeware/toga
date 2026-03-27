from platform import ios_ver

from .core_foundation import cf, kCFStringEncodingUTF8
from .sdk_version import get_sdk_version

bundle = cf.CFBundleGetMainBundle()
url = cf.CFBundleCopyBundleURL(bundle)
info_dict = cf.CFBundleCopyInfoDictionaryForURL(url)
key_cf = cf.CFStringCreateWithCString(
    None, b"UIDesignRequiresCompatibility", kCFStringEncodingUTF8
)
value_cf = cf.CFDictionaryGetValue(info_dict, key_cf)
if value_cf is None:
    value_py = None
else:
    value_py = bool(cf.CFBooleanGetValue(value_cf))
supports_liquid_glass = False
if value_py is True:
    supports_liquid_glass = False
elif value_py is False:
    supports_liquid_glass = True
else:
    supports_liquid_glass = int(get_sdk_version().split(".")[0]) >= 26

supports_liquid_glass = (
    supports_liquid_glass and int(ios_ver().release.split(".")[0]) >= 26
)

__all__ = ["supports_liquid_glass"]
