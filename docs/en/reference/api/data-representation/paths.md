{{ component_header("Paths") }}

## Usage

When Python code executes from the command line, the working directory is a known location - the location where the application was started. However, when executing GUI apps, the working directory varies between platforms. As a result, when specifying file paths, relative paths cannot be used, as there is no location to which they can be considered relative.

Complicating matters further, operating systems have conventions (and in some cases, hard restrictions) over where certain file types should be stored. For example, macOS provides the `~/Library/Application Support` folder; Linux encourages use of the `~/.config` folder (amongst others), and Windows provides the `AppData/Local` folder in the user's home directory. Application sandbox and security policies will sometimes prevent reading or writing files in any location other than these pre-approved locations.

To assist with finding an appropriate location to store application files, every Toga application instance has a [`paths`][toga.App.paths] attribute that returns an instance of [`Paths`][toga.paths.Paths]. This object provides known file system locations that are appropriate for storing files of given types, such as configuration files, log files, cache files, or user data.

Each location provided by the [`Paths`][toga.paths.Paths] object is a [`pathlib.Path`][] that can be used to construct a full file path. If required, additional subdirectories can be created under these locations. Toga will guarantee that the path provided *by Toga* will exist, but it is up you to create any desired subdirectory - if you want to create a `credentials/user.toml` configuration file, Toga will guarantee that the `apps.path.config` will exist, but you must take responsibility for creating the `credentials` subdirectory before saving `user.toml`.

In addition to these app-specific locations, the [`Paths`][toga.paths.Paths] object provides anchors for common user-space folders - the user's Desktop, Documents, Downloads and Pictures folders. These folders belong to the user, not the app, so Toga will *not* create them: if the folder doesn't exist on the device, or the platform doesn't provide the folder at all (as on mobile and web platforms), accessing the path raises a `RuntimeError`.

## Notes

- On macOS, the operating system may show a permission dialog the first time the app accesses the user's Desktop, Documents, Downloads or Pictures folder. This happens automatically on first file access; there is no API to request the permission in advance. If the user denies access, the path can still be obtained, but file operations in the folder will fail.
- On Linux, the user-space folder locations honor the `user-dirs.dirs` configuration created by the freedesktop `xdg-user-dirs` tool (folder names differ between languages). If there is no configuration for a folder, the matching `XDG_*_DIR` environment variable is used, falling back to the default English folder name in the user's home folder.
- On Windows, the user-space folder locations are obtained from the operating system, so folder redirection (e.g., by OneDrive) is honored.

## Reference

::: toga.paths.Paths
