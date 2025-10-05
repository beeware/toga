# Android

The Toga backend for Android is [`toga-android`](https://github.com/beeware/toga/tree/main/android).

## Prerequisites

`toga-android` requires Android SDK 24 (Android 7 / Nougat) or newer.

## Installation

`toga-android` must be manually installed into an Android project; The recommended approach for deploying `toga-android` is to use [Briefcase](https://briefcase.readthedocs.org) to package your app.

## Implementation details

The `toga-android` backend uses the [Android Java API](https://developer.android.com/reference), with [Material3 widgets](https://m3.material.io). It uses [Chaquopy](https://chaquo.com/chaquopy/) to provide a bridge to the native Android Java libraries and implement Java interfaces from Python.

## Platform-specific APIs

### Activities and Intents

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
