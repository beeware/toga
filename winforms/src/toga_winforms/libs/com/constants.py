from __future__ import annotations

from ctypes import Structure, c_int, c_ulong
from ctypes.wintypes import LPCWSTR
from enum import IntFlag
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from ctypes import _CData


class FileOpenOptions(IntFlag):
    FOS_UNKNOWN1 = 0x00000001
    FOS_OVERWRITEPROMPT = 0x00000002
    FOS_STRICTFILETYPES = 0x00000004
    FOS_NOCHANGEDIR = 0x00000008
    FOS_UNKNOWN2 = 0x00000010
    FOS_PICKFOLDERS = 0x00000020
    FOS_FORCEFILESYSTEM = 0x00000040
    FOS_ALLNONSTORAGEITEMS = 0x00000080
    FOS_NOVALIDATE = 0x00000100
    FOS_ALLOWMULTISELECT = 0x00000200
    FOS_UNKNOWN4 = 0x00000400
    FOS_PATHMUSTEXIST = 0x00000800
    FOS_FILEMUSTEXIST = 0x00001000
    FOS_CREATEPROMPT = 0x00002000
    FOS_SHAREAWARE = 0x00004000
    FOS_NOREADONLYRETURN = 0x00008000
    FOS_NOTESTFILECREATE = 0x00010000
    FOS_HIDEMRUPLACES = 0x00020000
    FOS_HIDEPINNEDPLACES = 0x00040000
    FOS_UNKNOWN5 = 0x00080000
    FOS_NODEREFERENCELINKS = 0x00100000
    FOS_UNKNOWN6 = 0x00200000
    FOS_UNKNOWN7 = 0x00400000
    FOS_UNKNOWN8 = 0x00800000
    FOS_UNKNOWN9 = 0x01000000
    FOS_DONTADDTORECENT = 0x02000000
    FOS_UNKNOWN10 = 0x04000000
    FOS_UNKNOWN11 = 0x08000000
    FOS_FORCESHOWHIDDEN = 0x10000000
    FOS_DEFAULTNOMINIMODE = 0x20000000
    FOS_FORCEPREVIEWPANEON = 0x40000000
    FOS_UNKNOWN12 = 0x80000000


# Shell Folder Get Attributes Options
SFGAOF = c_ulong


class SFGAO(IntFlag):
    SFGAO_CANCOPY = 0x00000001  # Objects can be copied.
    SFGAO_CANMOVE = 0x00000002  # Objects can be moved.
    SFGAO_CANLINK = 0x00000004  # Objects can be linked.
    SFGAO_STORAGE = 0x00000008  # Objects can be stored.
    SFGAO_CANRENAME = 0x00000010  # Objects can be renamed.
    SFGAO_CANDELETE = 0x00000020  # Objects can be deleted.
    SFGAO_HASPROPSHEET = 0x00000040  # Objects have property sheets.
    SFGAO_DROPTARGET = 0x00000100  # Objects are drop targets.
    SFGAO_CAPABILITYMASK = 0x00000177  # Mask for all capability flags.
    SFGAO_ENCRYPTED = 0x00002000  # Object is encrypted (use alt color).
    SFGAO_ISSLOW = 0x00004000  # Accessing this object is slow.
    SFGAO_GHOSTED = 0x00008000  # Object is ghosted (dimmed).
    SFGAO_LINK = 0x00010000  # Shortcut (link).
    SFGAO_SHARE = 0x00020000  # Shared.
    SFGAO_READONLY = 0x00040000  # Read-only.
    SFGAO_HIDDEN = 0x00080000  # Hidden object.
    SFGAO_DISPLAYATTRMASK = 0x000FC000  # Mask for display attributes.
    SFGAO_FILESYSANCESTOR = 0x10000000  # May contain children with file system folders.
    SFGAO_FOLDER = 0x20000000  # Is a folder.
    SFGAO_FILESYSTEM = 0x40000000  # Is part of the file system.
    SFGAO_HASSUBFOLDER = 0x80000000  # May contain subfolders.
    SFGAO_CONTENTSMASK = 0x80000000  # Mask for contents.
    SFGAO_VALIDATE = 0x01000000  # Invalidate cached information.
    SFGAO_REMOVABLE = 0x02000000  # Is a removable media.
    SFGAO_COMPRESSED = 0x04000000  # Object is compressed.
    SFGAO_BROWSABLE = 0x08000000  # Supports browsing.
    SFGAO_NONENUMERATED = 0x00100000  # Is not enumerated.
    SFGAO_NEWCONTENT = 0x00200000  # New content is present.
    SFGAO_CANMONIKER = 0x00400000  # Can create monikers for this item.
    SFGAO_HASSTORAGE = 0x00400000  # Supports storage interfaces.
    SFGAO_STREAM = 0x00400000  # Is a stream object.
    SFGAO_STORAGEANCESTOR = 0x00800000  # May contain children with storage folders.
    SFGAO_STORAGECAPMASK = 0x70C50008  # Mask for storage capability attributes.
    SFGAO_PKEYSFGAOMASK = (
        0x81044000  # Attributes that are part of the PKEY_SFGAOFlags property.
    )


class SIGDN(c_int):
    SIGDN_NORMALDISPLAY = 0x00000000
    SIGDN_PARENTRELATIVEPARSING = 0x80018001
    SIGDN_PARENTRELATIVEFORADDRESSBAR = 0x8001C001
    SIGDN_DESKTOPABSOLUTEPARSING = 0x80028000
    SIGDN_PARENTRELATIVEEDITING = 0x80031001
    SIGDN_DESKTOPABSOLUTEEDITING = 0x8004C000
    SIGDN_FILESYSPATH = 0x80058000
    SIGDN_URL = 0x80068000


class FDAP(c_int):
    FDAP_BOTTOM = 0x00000000
    FDAP_TOP = 0x00000001


class FDE_SHAREVIOLATION_RESPONSE(c_int):  # noqa: N801
    FDESVR_DEFAULT = 0x00000000
    FDESVR_ACCEPT = 0x00000001
    FDESVR_REFUSE = 0x00000002


FDE_OVERWRITE_RESPONSE = FDE_SHAREVIOLATION_RESPONSE


class COMDLG_FILTERSPEC(Structure):  # noqa: N801
    _fields_: Sequence[tuple[str, type[_CData]] | tuple[str, type[_CData], int]] = [
        ("pszName", LPCWSTR),
        ("pszSpec", LPCWSTR),
    ]
