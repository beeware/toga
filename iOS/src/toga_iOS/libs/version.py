import platform

IOS_VERSION = tuple(map(int, platform.release().split(".")))
