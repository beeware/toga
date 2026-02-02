{{ component_header("WebView", width=450) }}

## Usage

```python
import toga

webview = toga.WebView()

# Request a URL be loaded in the webview.
webview.url = "https://beeware.org"

# Load a URL, and wait (non-blocking) for the page to complete loading
await webview.load_url("https://beeware.org")

# Load static HTML content into the wevbiew.
webview.set_content("https://example.com", "<html>...</html>")
```

## System requirements  { #webview-system-requires }

- Using WebView on Windows 10 requires that your users have installed the [Edge WebView2 Evergreen Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download). This is installed by default on Windows 11.

- Using WebView on Linux requires that the user has installed the system packages for WebKit2, plus the GObject Introspection bindings for WebKit2. The name of the system package required is distribution dependent:
    - Ubuntu 20.04; Debian 11: `gir1.2-webkit2-4.0`
    - Ubuntu 22.04+; Debian 12+: `gir1.2-webkit2-4.1`
    - Fedora: `webkit2gtk4.1`
    - Arch/Manjaro: `webkit2gtk-4.1`
    - OpenSUSE Tumbleweed: `libwebkit2gtk3 typelib(WebKit2)`
    - FreeBSD: `webkit2-gtk3`

  WebView is not fully supported on GTK4. If you want to contribute to   the GTK4 WebView implementation, you will require v6.0 of the WebKit2   libraries. This is provided by `gir1.2-webkit-6.0` on Ubuntu/Debian,   and `webkitgtk6.0` on Fedora; for other distributions, consult your   distribution's platform documentation.

## Notes

- Due to app security restrictions, WebView can only display `http://` and `https://` URLs, not `file://` URLs. To serve local file content, run a web server on `localhost` using a background thread.

- On macOS 13.3 (Ventura) and later, the content inspector for your app can be opened by running Safari, [enabling the developer tools](https://support.apple.com/en-au/guide/safari/sfri20948/mac), and selecting your app's window from the "Develop" menu.  On macOS versions prior to Ventura, the content inspector is not enabled by default, and is only available when your code is packaged as a full macOS app (e.g., with Briefcase). To enable debugging, run:  > ```console > $ defaults write com.example.appname WebKitDeveloperExtras -bool true > ``` > > Substituting `com.example.appname` with the bundle ID for your > packaged app.

- On Android, use of the `on_navigation_starting` or `on_webview_load` handler requires adding `chaquopy.defaultConfig.staticProxy("toga_android.widgets.internal.webview")` to the `build_gradle_extra_content` section of your app's `pyproject.toml` configuration. Loading large (>2MB) HTML content from a string requires the same configuration change, as well as the addition of `"androidx.webkit:webkit:1.15.0"` to the `build_gradle_dependencies` section.

## Reference

::: toga.WebView

::: toga.widgets.webview.OnWebViewLoadHandler

::: toga.widgets.webview.OnNavigationStartingHandler
