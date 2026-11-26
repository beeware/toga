# Android

The Toga backend for Android is [`toga-android`](https://github.com/beeware/toga/tree/main/android).

## Prerequisites

`toga-android` requires Android SDK 24 (Android 7 / Nougat) or newer.

## Installation

`toga-android` must be manually installed into an Android project; The recommended approach for deploying `toga-android` is to use [Briefcase](https://briefcase.readthedocs.org) to package your app.

## Implementation details

The `toga-android` backend uses the [Android Java API](https://developer.android.com/reference), with [Material3 widgets](https://m3.material.io). It uses [Chaquopy](https://chaquo.com/chaquopy/) to provide a bridge to the native Android Java libraries and implement Java interfaces from Python.

## Platform-specific APIs

### Activities and intents

On Android, some interactions are managed using Activities, which are started using Intents.

Android's implementation of the [`toga.App`][] class includes the method [`start_activity()`][toga_android.app.App.start_activity], which can be used to start an activity.

To use this method, instantiate an instance of `android.content.Intent`; optionally, provide additional arguments, and a callback that will be invoked when the activity completes. For example, to dial a phone number with the `Intent.ACTION_DIAL` intent:

```python
from android.content import Intent
from android.net import Uri

intent = Intent(Intent.ACTION_DIAL)
intent.setData(Uri.parse("tel:0123456789"))


def number_dialed(result, data):
    # result is the status code (e.g., Activity.RESULT_OK)
    # data is the value returned by the activity.
    ...


# Assuming your toga.App app instance is called `app`
app._impl.start_activity(intent, on_complete=number_dialed)
```

### App lifecycle hooks

Android notifies an app of lifecycle events (such as the app becoming visible, moving to the background, or gaining input focus) by calling methods on a Java `Activity` class. Toga forwards these lifecycle events to methods on the Android `App` implementation class that are prefixed with `android_`. For example, the `onStop()` callback is handled by `android_onStop()` on the Android App class.

An app can hook into a lifecycle event by defining a custom subclass of the Android App implementation class, and registering it with [`toga.register_impl()`][toga.platform.register_impl]:

```python
import toga

if toga.backend == "toga_android":
    from toga_android.app import App as AndroidApp

    @toga.register_impl("App")
    class MyAndroidApp(AndroidApp):
        def android_onStop(self):
            # ... custom logic before default Toga implementation ...
            super().android_onStop()
            # ... custom logic after default Toga implementation ...
```

See [Registering implementations at runtime][register-impl-at-runtime] for more details.

Each hook receives the same arguments as the underlying `Activity` class. `android_onStart()`, `android_onResume()`, `android_onPause()`, `android_onStop()` and `android_onTopResumedActivityChanged()` already implement behavior required by Toga's cross-platform API (e.g., triggering `on_show`/`on_hide` or `on_gain_focus`/`on_lose_focus` on the window); if you override one of these, call the base implementation to preserve that behavior, as shown in the example above.

The following lifecycle hooks are available:

### Back navigation

By default, Android handles the Back button itself; at the root of an app, pressing Back sends the app to the background. If your app has its own idea of going "back" (for example, returning to a previous screen of content), you can handle Back yourself.

Android's implementation of the [`toga.App`][] class registers an AndroidX [`OnBackPressedCallback`](https://developer.android.com/reference/androidx/activity/OnBackPressedCallback) as `back_callback`. This callback is disabled by default. While it is enabled, pressing Back invokes [`android_handleOnBackPressed()`][toga_android.app.App.android_handleOnBackPressed] instead of Android's default behavior. Android needs to know whether your app will handle Back *before* the user presses it, so that it can show the right predictive back animation. Enable the callback when your app has somewhere to go back to, and disable it when it doesn't:

```python
import sys

import toga

if sys.platform == "android":
    from toga_android.app import App as AndroidApp

    @toga.register_impl("App")
    class MyAndroidApp(AndroidApp):
        def android_handleOnBackPressed(self):
            self.interface.show_main_screen()


class MyApp(toga.App):
    def startup(self): ...

    def show_detail_screen(self):
        self.main_window.content = self.detail_box
        if sys.platform == "android":
            self._impl.back_callback.setEnabled(True)

    def show_main_screen(self):
        self.main_window.content = self.main_box
        if sys.platform == "android":
            self._impl.back_callback.setEnabled(False)
```

## Reference

<!-- rumdl-disable MD013 MD022 MD023 -->
::: toga_android.app.App
    options:
        members:
            - android_handleOnBackPressed
            - android_onCreate
            - android_onStart
            - android_onRestart
            - android_onResume
            - android_onPause
            - android_onStop
            - android_onDestroy
            - android_onTopResumedActivityChanged
            - android_onConfigurationChanged
            - start_activity
<!-- rumdl-enable MD013 MD022 MD023 -->
