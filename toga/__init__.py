from __future__ import print_function, unicode_literals, absolute_import, division

import sys, os

from .constants import *

__all__ = [
    '__version__',
    'platform'
]

# Examples of valid version strings
# __version__ = '1.2.3.dev1'  # Development release 1
# __version__ = '1.2.3a1'     # Alpha Release 1
# __version__ = '1.2.3b1'     # Beta Release 1
# __version__ = '1.2.3rc1'    # RC Release 1
# __version__ = '1.2.3'       # Final Release
# __version__ = '1.2.3.post1' # Post Release 1

__version__ = '0.1.1'

platform = None

toga_locals = locals()


def set_platform(platform_name):
    "Configures toga to use the specfied platform module"
    # Purge any existing platform symbols in the toga module
    if toga_locals['platform']:
        for symbol in toga_locals['platform'].__all__:
            __all__.remove(symbol)
            toga_locals.pop(symbol)

    # Import the new platform module
    if platform_name == 'iOS':
        import toga_iOS as platform
    elif platform_name == 'cocoa':
        import toga_cocoa as platform
    elif platform_name == 'gtk':
        import toga_gtk as platform
    elif platform_name == 'win32':
        import toga_win32 as platform
    else:
        raise AttributeError('Unknown platform')

    # Set the new platform module into the module namespace
    toga_locals['platform'] = platform

    # Export all the symbols from the platform module
    toga_locals.update(dict(
        (symbol, getattr(platform, symbol))
        for symbol in toga_locals['platform'].__all__
    ))


# Attempt to autodetect and set the platform
if sys.platform == 'darwin':
    if os.environ.get('TARGET_IPHONE_SIMULATOR') or os.environ.get('TARGET_IPHONE'):
        set_platform('iOS')
    else:
        set_platform('cocoa')
elif sys.platform == 'linux2':
    set_platform('gtk')
elif sys.platform == 'win32':
    set_platform('win32')
else:
    raise NotImplementedError('Platform is not currently supported')
