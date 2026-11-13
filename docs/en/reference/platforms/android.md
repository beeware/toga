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

### `toga_android.App.start_activity()`

::: toga_android.app.App.start_activity
    options:
        show_root_heading: false

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

Android notifies an app of lifecycle events (such as the app becoming visible, moving to the background, or gaining input focus) by calling methods on the app's `Activity`. In an app packaged with Briefcase, this is the `MainActivity` class, which forwards a fixed set of these callbacks to Toga. Toga hands off each activity lifecycle callback it receives to a same-named method on the Android `App` implementation class, prefixed with `android_`. For example, the `onStop()` callback is handled by `android_onStop()` on the Android App class.

An app can hook into a lifecycle event by defining a custom subclass of a platform's App implementation class:

```python
import sys

if sys.platform == "android":
    from toga_android.app import App as AndroidApp

    class MyAndroidApp(AndroidApp):
        def android_onStop(self):
            # ... custom logic before default Toga implementation ...
            super().android_onStop()
            # ... custom logic after default Toga implementation ...
```

You can then direct your app to use this custom class by overriding the [`create()`][toga.App.create] method on your app to construct and return an instance of your custom App class when running on Android:

```python
class MyApp(toga.App):
    def create(self):
        if sys.platform == "android":
            return MyAndroidApp(interface=self)
        else:
            return super().create()

    def startup(self): ...
```

Each hook receives the same arguments as the underlying `Activity` callback. `android_onStart()`, `android_onResume()`, `android_onPause()`, `android_onStop()` and `android_onTopResumedActivityChanged()` already implement behavior required by Toga's cross-platform API (e.g., triggering `on_show`/`on_hide` or `on_gain_focus`/`on_lose_focus` on the window); if you override one of these, call the base implementation to preserve that behavior, as shown in the example above.

The following lifecycle hooks are available:

<!-- rumdl-disable MD013 MD022 MD023 -->
::: toga_android.app.App
    options:
        show_root_heading: false
        show_root_toc_entry: false
        members:
            - android_onCreate
            - android_onStart
            - android_onRestart
            - android_onResume
            - android_onPause
            - android_onStop
            - android_onDestroy
            - android_onTopResumedActivityChanged
            - android_onConfigurationChanged
