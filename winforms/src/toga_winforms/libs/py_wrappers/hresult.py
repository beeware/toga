from __future__ import annotations

from ctypes import HRESULT as ctypesHRESULT  # noqa: N811
from ctypes import c_long, get_last_error
from typing import TYPE_CHECKING, ClassVar, cast

if TYPE_CHECKING:
    from typing_extensions import Literal, Self  # pyright: ignore[reportMissingModuleSource]


class Win32OSError(OSError):
    ...


class HRESULT(ctypesHRESULT):
    FACILITY_CODES: ClassVar[dict[int, str]] = {
        0: "FACILITY_NULL",
        1: "FACILITY_RPC",
        2: "FACILITY_DISPATCH",
        3: "FACILITY_STORAGE",
        4: "FACILITY_ITF",
        7: "FACILITY_WIN32",
        8: "FACILITY_WINDOWS",
        9: "FACILITY_SECURITY",
        10: "FACILITY_CONTROL",
        11: "FACILITY_CERT",
        12: "FACILITY_INTERNET",
        13: "FACILITY_MEDIASERVER",
        14: "FACILITY_MSMQ",
        15: "FACILITY_SETUPAPI",
        16: "FACILITY_SCARD",
        17: "FACILITY_COMPLUS",
        18: "FACILITY_AAF",
        19: "FACILITY_URT",
        20: "FACILITY_ACS",
        21: "FACILITY_DPLAY",
        22: "FACILITY_UMI",
        23: "FACILITY_SXS",
        24: "FACILITY_WINDOWS_CE",
        25: "FACILITY_HTTP",
        26: "FACILITY_USERMODE_COMMONLOG",
        27: "FACILITY_WER",
        28: "FACILITY_USERMODE_FILTER_MANAGER",
        29: "FACILITY_BACKGROUNDCOPY",
        30: "FACILITY_CONFIGURATION",
        31: "FACILITY_STATE_MANAGEMENT",
        32: "FACILITY_METADIRECTORY",
        33: "FACILITY_SYSTEM_INTEGRITY",
        34: "FACILITY_VIRTUALIZATION",
        35: "FACILITY_VOLMGR",
        36: "FACILITY_BCD",
        37: "FACILITY_USERMODE_VHD",
        38: "FACILITY_USERMODE_HYPERVISOR",
        39: "FACILITY_USERMODE_VM",
        40: "FACILITY_USERMODE_VOLSNAP",
        41: "FACILITY_USERMODE_STORLIB",
        42: "FACILITY_USERMODE_LICENSING",
        43: "FACILITY_USERMODE_SMB",
        44: "FACILITY_USERMODE_VSS",
        45: "FACILITY_USERMODE_FILE_REPLICATION",
        46: "FACILITY_USERMODE_NDIS",
        47: "FACILITY_USERMODE_TPM",
        48: "FACILITY_USERMODE_NT",
        49: "FACILITY_USERMODE_USB",
        50: "FACILITY_USERMODE_NTOS",
        51: "FACILITY_USERMODE_COMPLUS",
        52: "FACILITY_USERMODE_NET",
        53: "FACILITY_USERMODE_CONFIGURATION_MANAGER",
        54: "FACILITY_USERMODE_COM",
        55: "FACILITY_USERMODE_DIRECTORY_SERVICE",
        56: "FACILITY_USERMODE_CMI",
        57: "FACILITY_USERMODE_LSA",
        58: "FACILITY_USERMODE_RPC",
        59: "FACILITY_USERMODE_IPSECVPN",
        60: "FACILITY_USERMODE_NETWORK_POLICY",
        61: "FACILITY_USERMODE_DNS_SERVER",
        62: "FACILITY_USERMODE_DNS_SERVER_ADMIN",
        63: "FACILITY_USERMODE_DNS_SERVER_CONFIGURATION",
        64: "FACILITY_USERMODE_DNS_SERVER_TUNING",
        65: "FACILITY_USERMODE_DNS_SERVER_ZONE",
        66: "FACILITY_USERMODE_DNS_SERVER_FORWARDER",
        67: "FACILITY_USERMODE_DNS_SERVER_REPLICATION",
        68: "FACILITY_USERMODE_DNS_SERVER_NDNC",
        69: "FACILITY_USERMODE_DNS_SERVER_FORWARDS",
        70: "FACILITY_USERMODE_DNS_SERVER_DS",
        71: "FACILITY_USERMODE_DNS_SERVER_ROOT_HINTS",
        72: "FACILITY_USERMODE_DNS_SERVER_ZONE_SOURCE",
        73: "FACILITY_USERMODE_DNS_SERVER_DATABASE",
        74: "FACILITY_USERMODE_DNS_SERVER_PROTOCOL",
        75: "FACILITY_USERMODE_DNS_SERVER_SERVICED",
        76: "FACILITY_USERMODE_DNS_SERVER_SOCKETS",
        77: "FACILITY_USERMODE_DNS_SERVER_SERVER_ADMIN",
        78: "FACILITY_USERMODE_DNS_SERVER_SOAP",
        79: "FACILITY_USERMODE_DNS_SERVER_ISAPI",
        80: "FACILITY_USERMODE_DNS_SERVER_WEB",
        81: "FACILITY_USERMODE_DNS_SERVER_SERVER",
        82: "FACILITY_USERMODE_DNS_SERVER_ADMIN_R2",
        83: "FACILITY_USERMODE_DNS_SERVER_ISAPI_FILTER",
        84: "FACILITY_USERMODE_DNS_SERVER_NDNC2",
        85: "FACILITY_USERMODE_DNS_SERVER_EVENTLOG",
        86: "FACILITY_USERMODE_DNS_SERVER_ADMIN2",
        87: "FACILITY_USERMODE_DNS_SERVER_ZONE2",
        88: "FACILITY_USERMODE_DNS_SERVER_NDNC3",
        89: "FACILITY_USERMODE_DNS_SERVER_SOCKETS2",
        90: "FACILITY_USERMODE_DNS_SERVER_ADMIN3",
        91: "FACILITY_USERMODE_DNS_SERVER_WEB2",
        92: "FACILITY_USERMODE_DNS_SERVER_ADMIN4",
        93: "FACILITY_USERMODE_DNS_SERVER_SERVER3",
        94: "FACILITY_USERMODE_DNS_SERVER_SOCKETS3",
        95: "FACILITY_USERMODE_DNS_SERVER_ADMIN5",
        96: "FACILITY_USERMODE_DNS_SERVER_SERVER4",
        97: "FACILITY_USERMODE_DNS_SERVER_ADMIN6",
        98: "FACILITY_USERMODE_DNS_SERVER_SOCKETS4",
        99: "FACILITY_USERMODE_DNS_SERVER_WEB3",
    }

    def __new__(
        cls, value: HRESULT | ctypesHRESULT | int | c_long | None = None
    ) -> Self:
        if value is None:
            converted_value = 0
        elif isinstance(value, int):
            converted_value = value
        elif isinstance(getattr(value, "value", None), int):
            converted_value = value.value
        else:
            raise TypeError(f"Invalid type for HRESULT: {type(value)}")
        instance = c_long(converted_value)
        instance.__class__ = cls
        return cast(cls, instance)

    def __init__(self, value: HRESULT | ctypesHRESULT | int | c_long | None = None):
        if value is None:
            self.value = 0
        elif isinstance(value, int):
            self.value = value
        elif isinstance(getattr(value, "value", None), int):
            self.value = value.value
        else:
            raise TypeError(f"Invalid type for HRESULT: {type(value)}")

    @staticmethod
    def to_hresult(value: int) -> int:
        """Convert WinError to HRESULT if necessary."""
        if value & 0x80000000:
            value &= 0xFFFFFFFF
        return value

    @staticmethod
    def from_hresult(value: int) -> int:
        """Convert HRESULT to WinError."""
        return value & 0xFFFFFFFF if value < 0 else value

    def decode(self):
        severity: int = (self >> 31) & 1
        facility: int = (self >> 16) & 0x1FFF
        code: int = self & 0xFFFF

        severity_str: Literal["Success", "Failure"] = "Success" if severity == 0 else "Failure"
        facility_str: str = HRESULT.FACILITY_CODES.get(facility, "Unknown Facility")

        return (
            f"HRESULT: 0x{self:08X}\n"
            f"Severity: {severity_str}\n"
            f"Facility: {facility_str} ({facility})\n"
            f"Code: 0x{code:04X} ({code})"
        )

    def __str__(self):
        return str(self.to_hresult(self.value))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(
        self, other: int | ctypesHRESULT
    ) -> bool:  # sourcery skip: assign-if-exp, reintroduce-else
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return self.value == other_int

    def __ne__(
        self, other: HRESULT | ctypesHRESULT | int | c_long
    ) -> bool:  # sourcery skip: assign-if-exp, reintroduce-else
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return self.value != other_int

    def __int__(self) -> int:
        return self.to_hresult(self.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def as_integer_ratio(self) -> tuple[int, int]:
        return (self.value, 1)

    def __mod__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> int:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return self.value % other_int

    def __divmod__(
        self, other: HRESULT | ctypesHRESULT | int | c_long
    ) -> tuple[int, int]:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return divmod(self.value, other_int)

    def __pow__(
        self, other: HRESULT | ctypesHRESULT | int | c_long, mod: int | None = None
    ) -> int:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        if mod is None:
            return pow(self.value, other_int)
        return pow(self.value, other_int, mod)

    def __rmod__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> int:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return other_int % self.to_hresult(self.value)

    def __rdivmod__(
        self, other: HRESULT | ctypesHRESULT | int | c_long
    ) -> tuple[int, int]:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return divmod(other_int, self.to_hresult(self.value))

    def __and__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> int:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return self.to_hresult(self.value) & other_int

    def __or__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> int:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return self.to_hresult(self.value) | other_int

    def __xor__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> int:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return self.to_hresult(self.value) ^ other_int

    def __lshift__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> int:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return self.to_hresult(self.value) << other_int

    def __rshift__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> int:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return self.to_hresult(self.value) >> other_int

    def __rand__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> int:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return other_int & self.value

    def __ror__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> int:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return other_int | self.value

    def __rxor__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> int:
        if isinstance(other, (HRESULT, ctypesHRESULT, c_long)):
            return self.to_hresult(other.value) ^ self.value
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return other_int ^ self.value

    def __rlshift__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> int:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return other_int << self.value

    def __rrshift__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> int:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return other_int >> self.value

    def __neg__(self) -> int:
        return -self.value

    def __pos__(self) -> int:
        return +self.value

    def __invert__(self) -> int:
        return ~self.value

    def __trunc__(self) -> int:
        return self.value

    def __round__(self, ndigits: int = 0) -> int:
        return round(self.value, ndigits)

    def __getnewargs__(self) -> tuple[int]:
        return (self.value,)

    def __lt__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> bool:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return self.value < other_int

    def __le__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> bool:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return self.value <= other_int

    def __gt__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> bool:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return self.value > other_int

    def __ge__(self, other: HRESULT | ctypesHRESULT | int | c_long) -> bool:
        if not isinstance(other, int) and (not hasattr(other, "value") or not isinstance(other.value, int)):
            return NotImplemented
        other_int = self.to_hresult(other.value if isinstance(other, (HRESULT, ctypesHRESULT, c_long)) else other)
        return self.value >= other_int

    def __float__(self) -> float:
        return float(self.value)

    def __abs__(self) -> int:
        return abs(self.value)

    def __bool__(self) -> bool:
        return bool(self.value)

    def __index__(self) -> int:
        return self.value

    def __format__(self, format_spec: str) -> str:
        if format_spec == "08X":
            return f"{self.to_hresult(self.value):08X}"
        return format(self.to_hresult(self.value), format_spec)

    def exception(self, short_desc: str | None = None) -> Win32OSError:
        return Win32OSError(self.to_hresult(self.value), decode_hresult(self), short_desc or "")

    @classmethod
    def raise_for_status(
        cls,
        hresult: HRESULT | ctypesHRESULT | Self | int | None = None,
        short_desc: str | None = None,
        *,
        ignore_s_false: bool = False,
    ):
        hresult = HRESULT(get_last_error() if hresult is None else hresult)
        hr: Self = hresult if isinstance(hresult, cls) else cls(hresult)
        if (hr == 1 and not ignore_s_false) or hr not in (HRESULT(0), HRESULT(1)):
            raise hr.exception(short_desc)
        return hresult


def decode_hresult(hresult: HRESULT | int) -> str:
    if isinstance(hresult, HRESULT):
        hresult = hresult.value
    severity: int = (hresult >> 31) & 1
    facility: int = (hresult >> 16) & 0x1FFF
    code: int = hresult & 0xFFFF

    severity_str: Literal["Success", "Failure"] = "Success" if severity == 0 else "Failure"
    facility_str = HRESULT.FACILITY_CODES.get(facility, "Unknown Facility")

    return (
        f"HRESULT: 0x{HRESULT.to_hresult(hresult):08X}\n"
        f"Severity: {severity_str}\n"
        f"Facility: {facility_str} ({facility})\n"
        f"Code: 0x{code:04X} ({code})"
    )


def print_hresult(hresult: HRESULT | int) -> None:
    print(decode_hresult(hresult))


def hresult_to_winerror(hresult: int) -> int:
    """Convert a positive HRESULT value to the corresponding WinError value."""
    return hresult - 0x100000000 if hresult & 0x80000000 else hresult


def winerror_to_hresult(winerror: int) -> int:
    """Convert a WinError value to the corresponding positive HRESULT value."""
    return winerror + 0x100000000 if winerror < 0 else winerror


S_OK = HRESULT(0)
S_FALSE = HRESULT(1)


if __name__ == "__main__":
    # Example usage:
    hr1 = HRESULT(10)
    hr2 = HRESULT(c_long(20))
    hr3 = HRESULT(ctypesHRESULT(30))

    print(hr1 == 10)
    print(hr2 > hr1)
    print(hr3 == ctypesHRESULT(30))
