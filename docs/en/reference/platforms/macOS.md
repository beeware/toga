# macOS

![image](../images/cocoa.png){ width="300px" }

/// caption

///

<!-- TODO: Update alt text -->

The Toga backend for macOS is [`toga-cocoa`](https://github.com/beeware/toga/tree/main/cocoa).

## Prerequisites { #macos-prerequisites }

`toga-cocoa` requires macOS 11 (Big Sur) or newer.

## Installation

`toga-cocoa` is installed automatically on macOS machines (machines that report `sys.platform == 'darwin'`), or can be manually installed by running invoking:

```console
$ python -m pip install toga-cocoa
```

## Implementation details

The `toga-cocoa` backend uses the [AppKit Objective-C API](https://developer.apple.com/documentation/appkit/), also known as Cocoa.

The native APIs are accessed using [Rubicon Objective-C](https://rubicon-objc.readthedocs.io/).

## Platform-specific APIs

### App lifecycle hooks

macOS notifies an app of lifecycle events (app launch, activation, hiding, termination, etc.) by calling methods on an `NSApplicationDelegate` instance. Toga's implementation of this delegate hands off every lifecycle notification it receives to a same-named method on `toga_cocoa`'s `App` implementation class, prefixed with `cocoa_`. For example, the `applicationDidBecomeActive:` notification is handled by `cocoa_applicationDidBecomeActive()`.

In the absence of a cross-platform API for these events, an app can hook into a lifecycle event by replacing the corresponding `cocoa_` method on `toga_cocoa`'s `App` class. Any method that isn't required for Toga's own cross-platform behavior does nothing by default, so it is always safe to override.

```python
import sys

if sys.platform == "darwin":
    from toga_cocoa.app import App as NativeApp

    def my_did_become_active(self, notification):
        # ... custom logic before base class implementation ...
        NativeApp.cocoa_applicationDidBecomeActive(self, notification)
        # ... custom logic after base class implementation ...

    NativeApp.cocoa_applicationDidBecomeActive = my_did_become_active
```

The override is applied to the `App` **class**, not to a specific app instance. This matters because of how Python binds methods: a plain function assigned directly to an instance attribute (e.g. `self._impl.cocoa_applicationDidBecomeActive = my_did_become_active`) is *not* bound as a method, so it would be called without `self`, and a function defined with a `self` parameter would raise a `TypeError`. Assigning to the class instead lets Python's normal method resolution bind `self` correctly. Since a Toga app only ever has one instance of its native app class, overriding at the class level has the same practical effect as overriding "for this app".

Each hook receives the same arguments as the underlying `NSApplicationDelegate` method (usually an `NSNotification` instance). `cocoa_applicationWillHide()`, `cocoa_applicationDidUnhide()` and `cocoa_applicationDidFinishLaunching()` already implement behavior required by Toga's cross-platform API (e.g. triggering `on_hide`/`on_show` on windows); if you override one of these, call the base implementation to preserve that behavior, as shown in the example above.

The following lifecycle hooks are available:

<!-- rumdl-disable MD013 MD022 MD023 -->
::: toga_cocoa.app.App
    options:
        show_root_heading: false
        show_root_toc_entry: false
        members:
            - cocoa_applicationWillFinishLaunching
            - cocoa_applicationDidFinishLaunching
            - cocoa_applicationWillBecomeActive
            - cocoa_applicationDidBecomeActive
            - cocoa_applicationWillResignActive
            - cocoa_applicationDidResignActive
            - cocoa_applicationWillHide
            - cocoa_applicationDidHide
            - cocoa_applicationWillUnhide
            - cocoa_applicationDidUnhide
            - cocoa_applicationDidChangeScreenParameters
            - cocoa_applicationShouldTerminate
            - cocoa_applicationWillTerminate
