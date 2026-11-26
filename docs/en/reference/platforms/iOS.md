# iOS

The Toga backend for iOS is [`toga-iOS`](https://github.com/beeware/toga/tree/main/iOS).

## Prerequisites

`toga-iOS` requires iOS 12 or newer.

## Installation

`toga-iOS` must be manually installed into an iOS project; The recommended approach for deploying `toga-iOS` is to use [Briefcase](https://briefcase.readthedocs.org) to package your app.

## Implementation details

The `toga-iOS` backend uses the [UIKit Objective-C API](https://developer.apple.com/documentation/uikit).

The native APIs are accessed using [Rubicon Objective-C](https://rubicon-objc.readthedocs.io/).

## Platform-specific APIs

### App lifecycle hooks

iOS notifies an app of app-level lifecycle events (launch, memory warnings, termination, etc.) by calling methods on a `UIApplicationDelegate`. Toga's implementation of this delegate hands off each lifecycle method it receives to a same-named method on the iOS `App` implementation class, prefixed with `uikit_`. For example, the `applicationDidReceiveMemoryWarning:` notification is handled by `uikit_applicationDidReceiveMemoryWarning()` on the iOS App class.

An app can hook into a lifecycle event by defining a custom subclass of the iOS App implementation class, and registering it with [`toga.register_impl()`][toga.platform.register_impl]:

```python
import toga

if toga.backend == "toga_iOS":
    from toga_iOS.app import App as iOSApp

    @toga.register_impl("App")
    class MyiOSApp(iOSApp):
        def uikit_application_didFinishLaunchingWithOptions(
            self, application, launchOptions
        ):
            # ... custom logic before default Toga implementation ...
            result = super().uikit_application_didFinishLaunchingWithOptions(
                application, launchOptions
            )
            # ... custom logic after default Toga implementation ...
            return result
```

See [Registering implementations at runtime][register-impl-at-runtime] for more details.

Each hook receives the same arguments as the underlying delegate method (the `UIApplication` instance, plus any additional arguments). `uikit_application_didFinishLaunchingWithOptions()` already implements behavior required by Toga's cross-platform API (creating the app and showing the main window); if you override it, call the base implementation and return its result, as shown in the example above.

Toga uses the scene-based lifecycle, so iOS does not deliver the deprecated app-level activation and background notifications (such as `applicationDidBecomeActive:` or `applicationDidEnterBackground:`); no hooks are provided for them.

The following lifecycle hooks are available:

<!-- rumdl-disable MD013 MD022 MD023 -->
::: toga_iOS.app.App
    options:
        show_root_heading: false
        show_root_toc_entry: false
        members:
            - uikit_application_willFinishLaunchingWithOptions
            - uikit_application_didFinishLaunchingWithOptions
            - uikit_applicationDidReceiveMemoryWarning
            - uikit_applicationSignificantTimeChange
            - uikit_applicationProtectedDataWillBecomeUnavailable
            - uikit_applicationProtectedDataDidBecomeAvailable
            - uikit_applicationWillTerminate
