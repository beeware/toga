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

iOS notifies an app of lifecycle events by calling methods on two delegates: a `UIApplicationDelegate` for app-level events (launch, memory warnings, termination, etc.), and a `UIWindowSceneDelegate` for scene-level events (activation, moving to the background or foreground, etc.). Toga's implementation of these delegates hands off every lifecycle method it receives to a same-named method on the iOS `App` implementation class, prefixed with `uikit_`. For example, the `sceneDidBecomeActive:` notification is handled by `uikit_sceneDidBecomeActive()` on the iOS App class.

An app can hook into a lifecycle event by defining a custom subclass of a platform's App implementation class:

```python
import sys

if sys.platform == "ios":
    from toga_iOS.app import App as iOSApp

    class MyiOSApp(iOSApp):
        def uikit_sceneDidEnterBackground(self, scene):
            # ... custom logic before default Toga implementation ...
            super().uikit_sceneDidEnterBackground(scene)
            # ... custom logic after default Toga implementation ...
```

You can then direct your app to use this custom class by overriding the [`create()`][toga.App.create] method on your app to construct and return an instance of your custom App class when running on iOS:

```python
class MyApp(toga.App):
    def create(self):
        if sys.platform == "ios":
            return MyiOSApp(interface=self)
        else:
            return super().create()

    def startup(self): ...
```

Each hook receives the same arguments as the underlying delegate method (the `UIApplication` or `UIScene` instance, plus any additional arguments). `uikit_application_didFinishLaunchingWithOptions()`, `uikit_scene_willConnectToSession_options()`, `uikit_sceneDidBecomeActive()`, `uikit_sceneWillResignActive()`, `uikit_sceneDidEnterBackground()` and `uikit_sceneWillEnterForeground()` already implement behavior required by Toga's cross-platform API (e.g. creating the app, or triggering `on_hide`/`on_show` on the window); if you override one of these, call the base implementation to preserve that behavior, as shown in the example above.

Toga uses the scene-based lifecycle, so iOS does not deliver the app-level activation and background notifications (such as `applicationDidBecomeActive:` or `applicationDidEnterBackground:`). Use the equivalent scene hooks instead.

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
            - uikit_scene_willConnectToSession_options
            - uikit_sceneDidDisconnect
            - uikit_sceneDidBecomeActive
            - uikit_sceneWillResignActive
            - uikit_sceneDidEnterBackground
            - uikit_sceneWillEnterForeground
