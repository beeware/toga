from __future__ import annotations

from enum import IntEnum  # noqa: INP001


class FSCTL(IntEnum):
    # Windows XP and Earlier
    FSCTL_REQUEST_OPLOCK_LEVEL_1 = 0x00090000
    """Requests an opportunistic lock (oplock) of level 1."""

    FSCTL_REQUEST_OPLOCK_LEVEL_2 = 0x00090004
    """Requests an opportunistic lock (oplock) of level 2."""

    FSCTL_REQUEST_BATCH_OPLOCK = 0x00090008
    """Requests a batch opportunistic lock (oplock)."""

    FSCTL_OPLOCK_BREAK_ACKNOWLEDGE = 0x0009000C
    """Acknowledges an oplock break."""

    FSCTL_OPBATCH_ACK_CLOSE_PENDING = 0x00090010
    """Acknowledges that an oplock break is pending."""

    FSCTL_OPLOCK_BREAK_NOTIFY = 0x00090014
    """Notifies about an oplock break."""

    FSCTL_LOCK_VOLUME = 0x00090018
    """Locks the volume."""

    FSCTL_UNLOCK_VOLUME = 0x0009001C
    """Unlocks the volume."""

    FSCTL_DISMOUNT_VOLUME = 0x00090020
    """Dismounts the volume."""

    FSCTL_IS_VOLUME_MOUNTED = 0x00090028
    """Checks if the volume is mounted."""

    FSCTL_IS_PATHNAME_VALID = 0x0009002C
    """Signals the file system driver not to perform any I/O boundary checks on partition read or write calls."""

    FSCTL_MARK_VOLUME_DIRTY = 0x00090030
    """Marks the volume as dirty."""

    FSCTL_QUERY_RETRIEVAL_POINTERS = 0x00090034
    """Queries retrieval pointers."""

    FSCTL_GET_COMPRESSION = 0x0009003C
    """Retrieves the current compression state of a file or directory on a volume whose file system supports per-stream compression."""

    FSCTL_SET_COMPRESSION = 0x00090040
    """Sets the compression state of a file or directory on a volume whose file system supports per-stream compression."""

    FSCTL_SET_BOOTLOADER_ACCESSED = 0x0009004C
    """Marks the bootloader as accessed."""

    FSCTL_OPLOCK_BREAK_ACK_NO_2 = 0x00090050
    """Acknowledges an oplock break without taking any further action."""

    FSCTL_INVALIDATE_VOLUMES = 0x00090054
    """Invalidates the volumes."""

    FSCTL_QUERY_FAT_BPB = 0x00090058
    """Retrieves the BIOS Parameter Block (BPB) for a FAT file system."""

    FSCTL_REQUEST_FILTER_OPLOCK = 0x0009005C
    """Requests a filter opportunistic lock (oplock)."""

    FSCTL_FILESYSTEM_GET_STATISTICS = 0x00090060
    """Retrieves file system statistics."""

    FSCTL_GET_NTFS_VOLUME_DATA = 0x00090064
    """Retrieves information about the specified NTFS file system volume."""

    FSCTL_GET_NTFS_FILE_RECORD = 0x00090068
    """Retrieves the first file record that is in use and is of a lesser than or equal ordinal value to the requested file reference number."""

    FSCTL_GET_VOLUME_BITMAP = 0x0009006F
    """Retrieves a bitmap of occupied and available clusters on a volume."""

    FSCTL_GET_RETRIEVAL_POINTERS = 0x00090073
    """Given a file handle, retrieves a data structure that describes the allocation and location on disk of a specific file, or, given a volume handle, the locations of bad clusters on a volume."""  # noqa: E501, W505

    FSCTL_MOVE_FILE = 0x00090074
    """Relocates one or more virtual clusters of a file from one logical cluster to another within the same volume. This operation is used during defragmentation."""

    FSCTL_IS_VOLUME_DIRTY = 0x00090078
    """Determines whether the volume's dirty bit is set, indicating that the file system may be in an inconsistent state."""

    FSCTL_ALLOW_EXTENDED_DASD_IO = 0x00090083
    """Allows file systems that reside on large storage devices to issue I/O operations that go beyond the 32-bit address range."""

    FSCTL_FIND_FILES_BY_SID = 0x0009008F
    """Finds files on a volume that belong to a specified security identifier (SID)."""

    FSCTL_SET_OBJECT_ID = 0x000900BC
    """Sets the object identifier for the specified file or directory."""

    FSCTL_GET_OBJECT_ID = 0x0009009C
    """Retrieves the object identifier for the specified file or directory."""

    FSCTL_DELETE_OBJECT_ID = 0x000900A0
    """Deletes the object identifier for the specified file or directory."""

    FSCTL_SET_REPARSE_POINT = 0x000900A4
    """Sets a reparse point on a file or directory."""

    FSCTL_GET_REPARSE_POINT = 0x000900A8
    """Retrieves the reparse point data associated with the file or directory identified by the specified handle."""

    FSCTL_DELETE_REPARSE_POINT = 0x000900AC
    """Deletes a reparse point from the specified file or directory."""

    FSCTL_ENUM_USN_DATA = 0x000900B0
    """Enumerates the update sequence number (USN) change journal data."""

    FSCTL_SECURITY_ID_CHECK = 0x000900B4
    """Performs a security ID check."""

    FSCTL_READ_USN_JOURNAL = 0x000900B8
    """Reads the update sequence number (USN) change journal."""

    FSCTL_SET_OBJECT_ID_EXTENDED = 0x000900C0
    """Sets extended information for an object identifier. This operation is part of the object identifier management on NTFS volumes."""

    FSCTL_CREATE_OR_GET_OBJECT_ID = 0x000900C3
    """Retrieves the object identifier for the specified file or directory. If no object identifier exists, this operation creates one."""

    FSCTL_SET_SPARSE = 0x000900C4
    """Marks the indicated file as sparse or not sparse. In a sparse file, large ranges of zeros may not require disk allocation."""

    FSCTL_SET_ZERO_DATA = 0x000980C8
    """Fills a specified range of a file with zeros (0)."""

    FSCTL_QUERY_ALLOCATED_RANGES = 0x000940CF
    """Scans a file or alternate stream looking for ranges that may contain nonzero data."""

    FSCTL_SET_ZERO_ON_DEALLOCATION = 0x00090194
    """Indicates an NTFS file system file handle should have its clusters filled with zeros when it is deallocated."""

    FSCTL_MARK_HANDLE = 0x000900FC
    """Marks a specified file or directory and its change journal record with information about changes to that file or directory."""

    FSCTL_GET_RETRIEVAL_POINTER_BASE = 0x00090098
    """Retrieves the base LCN (Logical Cluster Number) of the allocation unit."""

    FSCTL_IS_CSV_FILE = 0x0009016B
    """Determines whether a file is in a Cluster Shared Volume (CSV)."""

    FSCTL_INITIATE_REPAIR = 0x00090354
    """Triggers the NTFS file system to start a self-healing cycle on a single file."""

    FSCTL_SHRINK_VOLUME = 0x000902A4
    """Shrinks the volume."""

    FSCTL_TXFS_MODIFY_RM = 0x00090294
    """Modifies the Resource Manager (RM) for a transactional file system."""

    FSCTL_TXFS_QUERY_RM_INFORMATION = 0x000902A0
    """Queries Resource Manager (RM) information for a transactional file system."""

    FSCTL_TXFS_ROLLFORWARD_REDO = 0x000902B4
    """Performs a redo of a transaction during a rollforward operation."""

    FSCTL_TXFS_ROLLFORWARD_UNDO = 0x000902B8
    """Performs an undo of a transaction during a rollforward operation."""

    FSCTL_TXFS_START_RM = 0x000902BC
    """Starts the Resource Manager (RM) for a transactional file system."""

    FSCTL_TXFS_SHUTDOWN_RM = 0x000902C0
    """Shuts down the Resource Manager (RM) for a transactional file system."""

    FSCTL_TXFS_READ_BACKUP_INFORMATION = 0x000902C4
    """Reads backup information for a transactional file system."""

    FSCTL_TXFS_WRITE_BACKUP_INFORMATION = 0x000902C8
    """Writes backup information for a transactional file system."""

    FSCTL_TXFS_CREATE_SECONDARY_RM = 0x000902CC
    """Creates a secondary Resource Manager (RM) for a transactional file system."""

    FSCTL_TXFS_GET_METADATA_INFO = 0x000902D0
    """Gets metadata information for a transactional file system."""

    FSCTL_TXFS_GET_TRANSACTED_VERSION = 0x000902D4
    """Gets the transacted version of a file in a transactional file system."""

    FSCTL_TXFS_SAVEPOINT_INFORMATION = 0x000902E0
    """Gets savepoint information for a transactional file system."""

    FSCTL_TXFS_CREATE_MINIVERSION = 0x000902F0
    """Creates a mini version of a file in a transactional file system."""

    FSCTL_TXFS_TRANSACTION_ACTIVE = 0x00090318
    """Indicates whether a transaction is active in a transactional file system."""

    FSCTL_RESET_VOLUME_ALLOCATION_HINTS = 0x00090274
    """Resets volume allocation hints."""

    FSCTL_QUERY_USN_JOURNAL = 0x000900F4
    """Queries for information on the current update sequence number (USN) change journal, its records, and its capacity."""

    FSCTL_DELETE_USN_JOURNAL = 0x000900F8
    """Deletes the update sequence number (USN) change journal."""

    FSCTL_READ_FILE_USN_DATA = 0x000900EB
    """Retrieves the update sequence number (USN) change-journal information for the specified file or directory."""

    FSCTL_WRITE_USN_CLOSE_RECORD = 0x000900F0
    """Generates a close record in the USN change journal."""

    FSCTL_SIS_COPYFILE = 0x00090040
    """Performs a copy operation on a single instance store (SIS) volume."""

    FSCTL_SIS_LINK_FILES = 0x00090044
    """Links two files on a single instance store (SIS) volume."""

    FSCTL_GET_QUOTA_INFORMATION = 0x00090040
    """Retrieves quota information for the specified volume."""

    FSCTL_GET_ENCRYPTION = 0x00090062
    """Retrieves the encryption state of a file or directory on a volume that supports the Encrypting File System (EFS)."""

    FSCTL_SET_ENCRYPTION = 0x000900A7
    """Sets the encryption state of a file or directory on a volume that supports the Encrypting File System (EFS)."""

    FSCTL_SET_USN_JOURNAL = 0x000900F8
    """Creates an update sequence number (USN) change journal stream on a target volume, or modifies an existing change journal stream."""

    FSCTL_QUERY_LOCKS = 0x00094011
    """Queries for lock information on a file."""

    FSCTL_QUERY_SPARSE_FILE = 0x00094013
    """Queries whether the file is a sparse file."""

    FSCTL_SET_DEFECT_MANAGEMENT = 0x00090088
    """Disables or enables the defect management feature for the specified file. This feature is typically used for CD/DVD/Blu-ray media."""

    FSCTL_GET_OBJECT_ID_EXTENDED = 0x000900DB
    """Retrieves extended information for an object identifier."""

    FSCTL_DISABLE_LOCAL_BUFFERING = 0x0009008D
    """Disables local buffering for a file."""

    # Windows Vista
    FSCTL_GET_REPAIR = 0x00090274
    """Retrieves information about the NTFS file system's self-healing mechanism."""

    FSCTL_GET_RETRIEVAL_POINTERS_AND_REFCOUNT = 0x00090173
    """Retrieves a data structure that describes the allocation and reference count information for the specified file."""

    FSCTL_SET_SHORT_NAME_BEHAVIOR = 0x000980A4
    """Sets the short name behavior for a specified volume."""

    FSCTL_QUERY_ON_DISK_VOLUME_INFO = 0x0009013C
    """Queries information about the on-disk format of a volume."""

    FSCTL_SET_PURGE_FAILURE_MODE = 0x000980A8
    """Sets the purge failure mode for a specified volume."""

    # Windows 7
    FSCTL_DUPLICATE_EXTENTS_TO_FILE = 0x00098344
    """Instructs the file system to copy a range of file bytes on behalf of an application."""

    FSCTL_FILE_LEVEL_TRIM = 0x00098208
    """Indicates ranges within the specified file that do not need to be stored by the storage system."""

    FSCTL_GET_INTEGRITY_INFORMATION = 0x0009027C
    """Retrieves the integrity status of a file or directory on a ReFS volume."""

    FSCTL_GET_BOOT_AREA_INFO = 0x0009018C
    """Retrieves information about the boot area of a volume."""

    # Windows 8
    FSCTL_QUERY_PAGEFILE_ENCRYPTION = 0x0009019E
    """Queries the encryption state of a page file."""

    FSCTL_QUERY_STORAGE_CLASSES = 0x000902A0
    """Retrieves the storage tiers defined for a volume that supports data tiering."""

    FSCTL_CSV_QUERY_VETO_FILE_DIRECT_IO = 0x000902D1
    """Determines whether direct I/O is vetoed for a file in a Cluster Shared Volume (CSV)."""

    FSCTL_SET_INTEGRITY_INFORMATION = 0x0009C280
    """Sets the integrity status of a file or directory on a ReFS volume."""

    FSCTL_QUERY_REGION_INFO = 0x00090314
    """Retrieves storage tier regions defined for a volume that supports data tiering. This function returns detailed information about the regions in the tiered storage volume."""  # noqa: E501

    FSCTL_QUERY_FILE_SYSTEM_RECOGNITION = 0x00090318
    """Queries for file system recognition information on a volume."""

    FSCTL_GET_REFS_VOLUME_DATA = 0x00090364
    """Retrieves information about a ReFS volume."""

    FSCTL_INTEGRITY_CHECKPOINT = 0x00090394
    """Provides a mechanism to trigger an integrity checkpoint on a file or volume."""

    FSCTL_SCRUB_DATA = 0x0009035C
    """Scrubs the data on the volume to detect and potentially repair data corruption."""

    FSCTL_REPAIR_COPIES = 0x00090384
    """Repairs copies of files that are corrupt."""

    # Windows 10
    FSCTL_LOOKUP_STREAM_FROM_CLUSTER = 0x000902B1
    """Given a handle to a NTFS volume or a file on a NTFS volume, returns a chain of data structures that describes streams that occupy the specified clusters."""

    FSCTL_FILESYSTEM_GET_STATISTICS_EX = 0x00090334
    """Retrieves the information from various file system performance counters."""

    FSCTL_SET_REFS_FILE_STRICTLY_SEQUENTIAL = 0x000903DC
    """Sets the file as strictly sequential on ReFS volumes."""

    FSCTL_QUERY_USN_JOURNAL_EX = 0x000903F4
    """Provides extended information about the USN change journal."""

    # Unknown
    FSCTL_MAKE_MEDIA_COMPATIBLE = 0x0009804C
    FSCTL_QUERY_SPARING_INFO = 0x00098054
    FSCTL_SET_VOLUME_COMPRESSION_STATE = 0x00098060
    FSCTL_TXFS_READ_BACKUP_INFORMATION2 = 0x000980A0
    FSCTL_TXFS_WRITE_BACKUP_INFORMATION2 = 0x000980A4
    FSCTL_FILE_TYPE_NOTIFICATION = 0x000980A8
    FSCTL_CSV_GET_VOLUME_PATH_NAME = 0x000980AC
    FSCTL_CSV_GET_VOLUME_NAME_FOR_VOLUME_MOUNT_POINT = 0x000980B0
    FSCTL_CSV_GET_VOLUME_PATH_NAMES_FOR_VOLUME_NAME = 0x000980B4
    FSCTL_IS_FILE_ON_CSV_VOLUME = 0x000980B8
    FSCTL_QUERY_DEPENDENT_VOLUME = 0x000980BC
    FSCTL_SD_GLOBAL_CHANGE = 0x000980C0
    FSCTL_SET_PERSISTENT_VOLUME_STATE = 0x000980D0
    FSCTL_QUERY_PERSISTENT_VOLUME_STATE = 0x000980D4
    FSCTL_REQUEST_OPLOCK = 0x000980D8
    FSCTL_CSV_TUNNEL_REQUEST = 0x000980DC
    FSCTL_ENABLE_UPGRADE = 0x00090034
    FSCTL_FILE_PREFETCH = 0x000900E4

class IOCTL(IntEnum):
    # Storage IOCTL codes
    STORAGE_CHECK_VERIFY = 0x002D1400
    """Checks if the media is accessible."""

    STORAGE_CHECK_VERIFY2 = 0x002D1400
    """Verifies the media accessibility."""

    STORAGE_MEDIA_REMOVAL = 0x002D1401
    """Prevents or allows the removal of the media."""

    STORAGE_EJECT_MEDIA = 0x002D1402
    """Ejects the media from the device."""

    STORAGE_LOAD_MEDIA = 0x002D1403
    """Loads the media into the device."""

    STORAGE_LOAD_MEDIA2 = 0x002D1403
    """Loads the media into the device (alternative)."""

    STORAGE_RESERVE = 0x002D1404
    """Reserves the device for exclusive use."""

    STORAGE_RELEASE = 0x002D1405
    """Releases the reserved device."""

    STORAGE_FIND_NEW_DEVICES = 0x002D1406
    """Scans for new storage devices."""

    STORAGE_EJECTION_CONTROL = 0x002D1450
    """Controls the ejection mechanism of the media."""

    STORAGE_MCN_CONTROL = 0x002D1451
    """Controls the media change notification feature."""

    STORAGE_GET_MEDIA_TYPES = 0x002D1500
    """Retrieves the media types supported by the device."""

    STORAGE_GET_MEDIA_TYPES_EX = 0x002D1501
    """Retrieves extended information about supported media types."""

    STORAGE_GET_MEDIA_SERIAL_NUMBER = 0x002D1504
    """Retrieves the serial number of the media."""

    STORAGE_GET_HOTPLUG_INFO = 0x002D1505
    """Retrieves hotplug information for the device."""

    STORAGE_SET_HOTPLUG_INFO = 0x002D1506
    """Sets hotplug information for the device."""

    STORAGE_RESET_BUS = 0x002D1600
    """Resets the bus on which the storage device is connected."""

    STORAGE_RESET_DEVICE = 0x002D1601
    """Resets the storage device."""

    STORAGE_BREAK_RESERVATION = 0x002D1605
    """Breaks the reservation on a storage device."""

    STORAGE_PERSISTENT_RESERVE_IN = 0x002D1606
    """Issues a persistent reserve in command to the device."""

    STORAGE_PERSISTENT_RESERVE_OUT = 0x002D1607
    """Issues a persistent reserve out command to the device."""

    STORAGE_GET_DEVICE_NUMBER = 0x002D1640
    """Retrieves the device number of the storage device."""

    STORAGE_PREDICT_FAILURE = 0x002D1680
    """Predicts potential failure of the storage device."""

    STORAGE_READ_CAPACITY = 0x002D1690
    """Reads the capacity of the storage device."""

    # Disk IOCTL codes
    DISK_GET_DRIVE_GEOMETRY = 0x00070000
    """Retrieves the geometry of the disk drive."""

    DISK_GET_PARTITION_INFO = 0x00070001
    """Retrieves partition information for the disk."""

    DISK_SET_PARTITION_INFO = 0x00070002
    """Sets partition information for the disk."""

    DISK_GET_DRIVE_LAYOUT = 0x00070003
    """Retrieves the drive layout of the disk."""

    DISK_SET_DRIVE_LAYOUT = 0x00070004
    """Sets the drive layout of the disk."""

    DISK_VERIFY = 0x00070005
    """Verifies the integrity of a region of the disk."""

    DISK_FORMAT_TRACKS = 0x00070006
    """Formats the specified tracks on the disk."""

    DISK_REASSIGN_BLOCKS = 0x00070007
    """Reassigns bad blocks on the disk."""

    DISK_PERFORMANCE = 0x00070008
    """Retrieves performance data for the disk."""

    DISK_IS_WRITABLE = 0x00070009
    """Checks if the disk is writable."""

    DISK_LOGGING = 0x0007000A
    """Controls logging on the disk."""

    DISK_FORMAT_TRACKS_EX = 0x0007000B
    """Formats the specified tracks on the disk with extended options."""

    DISK_HISTOGRAM_STRUCTURE = 0x0007000C
    """Retrieves the histogram structure for disk performance analysis."""

    DISK_HISTOGRAM_DATA = 0x0007000D
    """Retrieves histogram data for disk performance analysis."""

    DISK_HISTOGRAM_RESET = 0x0007000E
    """Resets the histogram data on the disk."""

    DISK_REQUEST_STRUCTURE = 0x0007000F
    """Retrieves the request structure for the disk."""

    DISK_REQUEST_DATA = 0x00070010
    """Retrieves request data for the disk."""

    DISK_PERFORMANCE_OFF = 0x00070018
    """Disables performance monitoring on the disk."""

    DISK_CONTROLLER_NUMBER = 0x00070011
    """Retrieves the controller number for the disk."""

    SMART_GET_VERSION = 0x00070020
    """Retrieves the version of the SMART (Self-Monitoring, Analysis, and Reporting Technology) feature."""

    SMART_SEND_DRIVE_COMMAND = 0x00070021
    """Sends a command to the drive using the SMART feature."""

    SMART_RCV_DRIVE_DATA = 0x00070022
    """Receives data from the drive using the SMART feature."""

    DISK_GET_PARTITION_INFO_EX = 0x00070012
    """Retrieves extended partition information for the disk."""

    DISK_SET_PARTITION_INFO_EX = 0x00070013
    """Sets extended partition information for the disk."""

    DISK_GET_DRIVE_LAYOUT_EX = 0x00070014
    """Retrieves extended drive layout information for the disk."""

    DISK_SET_DRIVE_LAYOUT_EX = 0x00070015
    """Sets extended drive layout information for the disk."""

    DISK_CREATE_DISK = 0x00070016
    """Creates a new disk layout."""

    DISK_GET_LENGTH_INFO = 0x00070017
    """Retrieves the length information of the disk."""

    DISK_GET_DRIVE_GEOMETRY_EX = 0x00070028
    """Retrieves extended geometry information for the disk."""

    DISK_REASSIGN_BLOCKS_EX = 0x00070029
    """Reassigns bad blocks on the disk with extended options."""

    DISK_UPDATE_DRIVE_SIZE = 0x00070032
    """Updates the size information of the disk."""

    DISK_GROW_PARTITION = 0x00070034
    """Grows the partition on the disk."""

    DISK_GET_CACHE_INFORMATION = 0x00070035
    """Retrieves cache information for the disk."""

    DISK_SET_CACHE_INFORMATION = 0x00070036
    """Sets cache information for the disk."""

    OBSOLETE_DISK_GET_WRITE_CACHE_STATE = 0x00070037
    """Obsolete. Previously retrieved the write cache state of the disk."""

    DISK_DELETE_DRIVE_LAYOUT = 0x00070040
    """Deletes the drive layout on the disk."""

    DISK_UPDATE_PROPERTIES = 0x00070050
    """Updates the properties of the disk."""

    DISK_FORMAT_DRIVE = 0x000700F3
    """Formats the entire drive."""

    DISK_SENSE_DEVICE = 0x000700F8
    """Senses the device status for the disk."""

    DISK_CHECK_VERIFY = 0x00070200
    """Checks if the disk is accessible."""

    DISK_MEDIA_REMOVAL = 0x00070201
    """Controls the removal of media from the disk."""

    DISK_EJECT_MEDIA = 0x00070202
    """Ejects the media from the disk."""

    DISK_LOAD_MEDIA = 0x00070203
    """Loads media into the disk."""

    DISK_RESERVE = 0x00070204
    """Reserves the disk for exclusive use."""

    DISK_RELEASE = 0x00070205
    """Releases the reserved disk."""

    DISK_FIND_NEW_DEVICES = 0x00070206
    """Scans for new devices connected to the disk."""

    DISK_GET_MEDIA_TYPES = 0x00070300
    """Retrieves the media types supported by the disk."""

    DISK_RESET_SNAPSHOT_INFO = 0x00070084
    """Resets snapshot information on the disk."""

    # Changer IOCTL codes
    CHANGER_GET_PARAMETERS = 0x00090000
    """Retrieves the parameters of the media changer device."""

    CHANGER_GET_STATUS = 0x00090001
    """Retrieves the current status of the media changer device."""

    CHANGER_GET_PRODUCT_DATA = 0x00090002
    """Retrieves product data for the media changer device."""

    CHANGER_SET_ACCESS = 0x00090004
    """Sets access control for the media changer device."""

    CHANGER_GET_ELEMENT_STATUS = 0x00090005
    """Retrieves the status of elements in the media changer."""

    CHANGER_INITIALIZE_ELEMENT_STATUS = 0x00090006
    """Initializes the status of elements in the media changer."""

    CHANGER_SET_POSITION = 0x00090007
    """Sets the position of elements within the media changer."""

    CHANGER_EXCHANGE_MEDIUM = 0x00090008
    """Exchanges media between two slots in the media changer."""

    CHANGER_MOVE_MEDIUM = 0x00090009
    """Moves media from one slot to another within the media changer."""

    CHANGER_LOCK_UNLOCK_ELEMENT = 0x0009000A
    """Locks or unlocks an element in the media changer."""

    CHANGER_POSITION_ELEMENT = 0x0009000B
    """Positions an element in the media changer."""

    CHANGER_RESERVE = 0x0009000C
    """Reserves the media changer for exclusive use."""

    CHANGER_RELEASE = 0x0009000D
    """Releases the reserved media changer."""

    CHANGER_EXCHANGE_MEDIUM_IN = 0x0009000E
    """Exchanges media in from an external slot to the media changer."""

    CHANGER_EXCHANGE_MEDIUM_OUT = 0x0009000F
    """Exchanges media out from the media changer to an external slot."""

    CHANGER_GET_ELEMENT_STATUS_IN = 0x00090010
    """Retrieves status information for input elements in the media changer."""

    CHANGER_GET_ELEMENT_STATUS_OUT = 0x00090011
    """Retrieves status information for output elements in the media changer."""

    CHANGER_MOVE_MEDIUM_IN = 0x00090012
    """Moves media from an external input slot into the media changer."""

    CHANGER_MOVE_MEDIUM_OUT = 0x00090013
    """Moves media from the media changer to an external output slot."""

    CHANGER_PREPARE_ELEMENT_FOR_ACCESS = 0x00090014
    """Prepares an element in the media changer for access."""

    CHANGER_READ_ELEMENT_STATUS = 0x00090015
    """Reads the status of an element in the media changer."""

    CHANGER_CALIBRATE = 0x00090016
    """Calibrates the elements of the media changer."""

    CHANGER_SET_ACCESS_CONTROL = 0x00090017
    """Sets access control permissions for the media changer."""

    CHANGER_GET_POSITION = 0x00090018
    """Retrieves the current position of elements in the media changer."""

    CHANGER_GET_PRODUCT_DATA_EX = 0x00090019
    """Retrieves extended product data for the media changer device."""

    CHANGER_SET_POSITION_EX = 0x0009001A
    """Sets the position of elements within the media changer with extended options."""

    CHANGER_EXCHANGE_MEDIUM_EX = 0x0009001B
    """Exchanges media between slots in the media changer with extended options."""

    CHANGER_LOCK_UNLOCK_ELEMENT_EX = 0x0009001C
    """Locks or unlocks an element in the media changer with extended options."""

    CHANGER_SET_ACCESS_EX = 0x0009001D
    """Sets access control permissions for the media changer with extended options."""

    CHANGER_PREPARE_ELEMENT_FOR_ACCESS_EX = 0x0009001E
    """Prepares an element in the media changer for access with extended options."""

    CHANGER_EXCHANGE_MEDIUM_IN_EX = 0x0009001F
    """Exchanges media in from an external slot to the media changer with extended options."""

    CHANGER_EXCHANGE_MEDIUM_OUT_EX = 0x00090020
    """Exchanges media out from the media changer to an external slot with extended options."""

    CHANGER_MOVE_MEDIUM_IN_EX = 0x00090021
    """Moves media from an external input slot into the media changer with extended options."""

    CHANGER_MOVE_MEDIUM_OUT_EX = 0x00090022
    """Moves media from the media changer to an external output slot with extended options."""

    CHANGER_CALIBRATE_EX = 0x00090023
    """Calibrates the elements of the media changer with extended options."""

    CHANGER_GET_STATUS_EX = 0x00090024
    """Retrieves the current status of the media changer with extended options."""

    CHANGER_GET_ELEMENT_STATUS_IN_EX = 0x00090025
    """Retrieves status information for input elements in the media changer with extended options."""

    CHANGER_GET_ELEMENT_STATUS_OUT_EX = 0x00090026
    """Retrieves status information for output elements in the media changer with extended options."""

    CHANGER_READ_ELEMENT_STATUS_EX = 0x00090027
    """Reads the status of an element in the media changer with extended options."""

    CHANGER_REINITIALIZE_TRANSPORT = 0x0009000A
    CHANGER_QUERY_VOLUME_TAGS = 0x0009000B

    # Tape IOCTL codes
    TAPE_ERASE = 0x00160000
    """Erases the tape media."""

    TAPE_PREPARE = 0x00160001
    """Prepares the tape drive for an operation."""

    TAPE_WRITE_MARKS = 0x00160002
    """Writes marks on the tape media."""

    TAPE_GET_POSITION = 0x00160003
    """Retrieves the current position of the tape media."""

    TAPE_SET_POSITION = 0x00160004
    """Sets the position of the tape media."""

    TAPE_GET_DRIVE_PARAMS = 0x00160005
    """Retrieves the parameters of the tape drive."""

    TAPE_SET_DRIVE_PARAMS = 0x00160006
    """Sets the parameters of the tape drive."""

    TAPE_GET_MEDIA_PARAMS = 0x00160007
    """Retrieves the parameters of the tape media."""

    TAPE_SET_MEDIA_PARAMS = 0x00160008
    """Sets the parameters of the tape media."""

    TAPE_GET_STATUS = 0x00160009
    """Retrieves the current status of the tape drive."""

    TAPE_GET_MEDIA_TYPES = 0x0016000A
    """Retrieves the media types supported by the tape drive."""

    TAPE_QUERY_DRIVE_PARAMETERS = 0x0016000B
    """Queries the drive parameters of the tape drive."""

    TAPE_QUERY_MEDIA_CAPACITY = 0x0016000C
    """Queries the media capacity of the tape media."""

    TAPE_PREPARE_EX = 0x0016000D
    """Prepares the tape drive for an operation with extended options."""

    TAPE_SET_POSITION_EX = 0x0016000E
    """Sets the position of the tape media with extended options."""

    TAPE_ERASE_EX = 0x0016000F
    """Erases the tape media with extended options."""

    TAPE_SET_DRIVE_PARAMS_EX = 0x00160010
    """Sets the parameters of the tape drive with extended options."""

    TAPE_SET_MEDIA_PARAMS_EX = 0x00160011
    """Sets the parameters of the tape media with extended options."""

    TAPE_WRITE_MARKS_EX = 0x00160012
    """Writes marks on the tape media with extended options."""

    TAPE_GET_DRIVE_PARAMS_EX = 0x00160013
    """Retrieves the parameters of the tape drive with extended options."""

    TAPE_GET_MEDIA_PARAMS_EX = 0x00160014
    """Retrieves the parameters of the tape media with extended options."""

    TAPE_GET_POSITION_EX = 0x00160015
    """Retrieves the current position of the tape media with extended options."""

    TAPE_GET_STATUS_EX = 0x00160016
    """Retrieves the current status of the tape drive with extended options."""
    # USB IOCTL codes
    USB_GET_NODE_INFORMATION = 0x00220040
    """Retrieves information about a USB node (hub or port)."""

    USB_GET_NODE_CONNECTION_INFORMATION = 0x00220041
    """Retrieves information about a connection to a USB node."""

    USB_GET_DESCRIPTOR_FROM_NODE_CONNECTION = 0x00220042
    """Retrieves a descriptor for a USB node connection."""

    USB_GET_NODE_CONNECTION_NAME = 0x00220044
    """Retrieves the name of a USB node connection."""

    USB_DIAG_IGNORE_HUBS_ON = 0x00220045
    """Enables diagnostic mode that ignores USB hubs."""

    USB_DIAG_IGNORE_HUBS_OFF = 0x00220046
    """Disables diagnostic mode that ignores USB hubs."""

    USB_GET_NODE_CONNECTION_DRIVERKEY_NAME = 0x00220047
    """Retrieves the driver key name for a USB node connection."""

    USB_GET_HUB_CAPABILITIES = 0x00220048
    """Retrieves the capabilities of a USB hub."""

    USB_GET_NODE_CONNECTION_ATTRIBUTES = 0x00220049
    """Retrieves the attributes of a USB node connection."""

    USB_GET_NODE_CONNECTION_INFORMATION_EX = 0x00220050
    """Retrieves extended information about a connection to a USB node."""

    USB_RESET_HUB = 0x00220051
    """Resets a USB hub."""

    USB_GET_HUB_CAPABILITIES_EX = 0x00220052
    """Retrieves extended capabilities of a USB hub."""

    USB_CYCLE_PORT = 0x00220053
    """Cycles the power of a USB port."""

    USB_GET_PORT_CONNECTOR_PROPERTIES = 0x00220054
    """Retrieves the properties of a USB port connector."""

    USB_GET_NODE_INFORMATION_EX = 0x00220055
    """Retrieves extended information about a USB node (hub or port)."""

    USB_GET_NODE_CONNECTION_INFORMATION_EX_V2 = 0x00220056
    """Retrieves additional extended information about a USB node connection."""

    USB_RESET_PORT = 0x00220057
    """Resets a USB port."""

    USB_HUB_CYCLE_PORT = 0x00220058
    """Cycles the power of a USB hub port."""

    USB_GET_NODE_CONNECTION_INFORMATION_EX_V2_1 = 0x00220059
    """Retrieves extended information about a USB node connection, version 2.1."""

    USB_GET_NODE_CONNECTION_DRIVERKEY_NAME_EX = 0x00220060
    """Retrieves the driver key name for a USB node connection with extended options."""

    USB_GET_DESCRIPTOR_FROM_NODE_CONNECTION_EX = 0x00220061
    """Retrieves a descriptor for a USB node connection with extended options."""

    USB_GET_NODE_INFORMATION_EX_V2 = 0x00220062
    """Retrieves additional extended information about a USB node, version 2."""

    USB_GET_NODE_INFORMATION_EX_V2_1 = 0x00220063
    """Retrieves extended information about a USB node, version 2.1."""

    USB_GET_NODE_CONNECTION_INFORMATION_EX_V2_2 = 0x00220064
    """Retrieves additional extended information about a USB node connection, version 2.2."""

    USB_GET_NODE_INFORMATION_EX_V3 = 0x00220065
    """Retrieves extended information about a USB node, version 3."""

    USB_HUB_RESET = 0x00220066
    """Resets a USB hub."""

    USB_HUB_RESET_EX = 0x00220067
    """Resets a USB hub with extended options."""

    USB_HUB_GET_NODE_INFORMATION = 0x00220068
    """Retrieves information about a USB hub node."""

    USB_HUB_GET_NODE_INFORMATION_EX = 0x00220069
    """Retrieves extended information about a USB hub node."""

    USB_HUB_RESET_PORT = 0x00220070
    """Resets a USB hub port."""

    USB_HUB_RESET_PORT_EX = 0x00220071
    """Resets a USB hub port with extended options."""

    USB_GET_NODE_INFORMATION_EX_V3_1 = 0x00220072
    """Retrieves extended information about a USB node, version 3.1."""

    USB_GET_NODE_CONNECTION_INFORMATION_EX_V3 = 0x00220073
    """Retrieves extended information about a USB node connection, version 3."""

    USB_GET_NODE_INFORMATION_EX_V3_2 = 0x00220074
    """Retrieves additional extended information about a USB node, version 3.2."""

    USB_HUB_RESET_EX_V2 = 0x00220075
    """Resets a USB hub with extended options, version 2."""

    USB_HUB_CYCLE_PORT_EX = 0x00220076
    """Cycles the power of a USB hub port with extended options."""

    USB_GET_PORT_CONNECTOR_PROPERTIES_EX = 0x00220077
    """Retrieves the properties of a USB port connector with extended options."""

    USB_GET_NODE_CONNECTION_INFORMATION_EX_V3_3 = 0x00220078
    """Retrieves additional extended information about a USB node connection, version 3.3."""

    USB_HUB_RESET_PORT_EX_V2 = 0x00220079
    """Resets a USB hub port with extended options, version 2."""

    # Serial IOCTL codes
    SERIAL_LSRMST_INSERT = 0x0001001F
    """Inserts Line Status Register (LSR) and Modem Status Register (MST) data into the input stream."""

    SERENUM_EXPOSE_HARDWARE = 0x00010080
    """Exposes the hardware associated with the serial enumerator."""

    SERENUM_REMOVE_HARDWARE = 0x00010081
    """Removes the hardware associated with the serial enumerator."""

    SERENUM_PORT_DESC = 0x00010082
    """Retrieves the port description for the serial enumerator."""

    SERENUM_GET_PORT_NAME = 0x00010083
    """Retrieves the port name for the serial enumerator."""

    # AVIO IOCTL codes
    AVIO_ALLOCATE_STREAM = 0x00060001
    """Allocates a stream for AVIO."""

    AVIO_FREE_STREAM = 0x00060002
    """Frees a previously allocated stream for AVIO."""

    AVIO_MODIFY_STREAM = 0x00060003
    """Modifies settings of a stream allocated for AVIO."""

    # Volume IOCTL codes
    VOLUME_GET_VOLUME_DISK_EXTENTS = 0x00560000
    """Retrieves disk extents for the specified volume."""

    VOLUME_ONLINE = 0x00560002
    """Brings the specified volume online."""

    VOLUME_OFFLINE = 0x00560003
    """Takes the specified volume offline."""

    VOLUME_IS_CLUSTERED = 0x0056000C
    """Checks if the specified volume is part of a cluster."""

    VOLUME_GET_GPT_ATTRIBUTES = 0x0056000E
    """Retrieves GPT attributes of the specified volume."""
