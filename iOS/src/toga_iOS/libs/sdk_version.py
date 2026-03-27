import ctypes

MH_MAGIC = 0xFEEDFACE
MH_MAGIC_64 = 0xFEEDFACF

LC_BUILD_VERSION = 0x32


class MachHeader32(ctypes.Structure):
    _fields_ = [
        ("magic", ctypes.c_uint32),
        ("cputype", ctypes.c_uint32),
        ("cpusubtype", ctypes.c_uint32),
        ("filetype", ctypes.c_uint32),
        ("ncmds", ctypes.c_uint32),
        ("sizeofcmds", ctypes.c_uint32),
        ("flags", ctypes.c_uint32),
    ]


class MachHeader64(ctypes.Structure):
    _fields_ = [
        ("magic", ctypes.c_uint32),
        ("cputype", ctypes.c_uint32),
        ("cpusubtype", ctypes.c_uint32),
        ("filetype", ctypes.c_uint32),
        ("ncmds", ctypes.c_uint32),
        ("sizeofcmds", ctypes.c_uint32),
        ("flags", ctypes.c_uint32),
        ("reserved", ctypes.c_uint32),
    ]


class LoadCommand(ctypes.Structure):
    _fields_ = [
        ("cmd", ctypes.c_uint32),
        ("cmdsize", ctypes.c_uint32),
    ]


class BuildVersionCommand(ctypes.Structure):
    _fields_ = [
        ("cmd", ctypes.c_uint32),
        ("cmdsize", ctypes.c_uint32),
        ("platform", ctypes.c_uint32),
        ("minos", ctypes.c_uint32),
        ("sdk", ctypes.c_uint32),
        ("ntools", ctypes.c_uint32),
    ]


libc = ctypes.CDLL(None)
_dyld_get_image_header = libc._dyld_get_image_header
_dyld_get_image_header.restype = ctypes.c_void_p
_dyld_get_image_header.argtypes = [ctypes.c_uint32]


def decode_version(v):
    return f"{v >> 16}.{(v >> 8) & 0xFF}.{v & 0xFF}"


def get_sdk_version():
    mh_ptr = _dyld_get_image_header(0)
    magic = ctypes.c_uint32.from_address(mh_ptr).value

    if magic == MH_MAGIC_64:
        header = MachHeader64.from_address(mh_ptr)
        cmd_ptr = mh_ptr + ctypes.sizeof(MachHeader64)
    elif magic == MH_MAGIC:
        header = MachHeader32.from_address(mh_ptr)
        cmd_ptr = mh_ptr + ctypes.sizeof(MachHeader32)
    else:
        return None

    for _ in range(header.ncmds):
        lc = LoadCommand.from_address(cmd_ptr)

        if lc.cmd == LC_BUILD_VERSION:
            cmd = BuildVersionCommand.from_address(cmd_ptr)
            return decode_version(cmd.sdk)

        cmd_ptr += lc.cmdsize

    return None


__all__ = ["get_sdk_version"]
