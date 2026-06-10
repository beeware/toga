# iOS

The Toga backend for iOS is [`toga-iOS`](https://github.com/beeware/toga/tree/main/iOS).

## Prerequisites

`toga-iOS` requires iOS 12 or newer.

Compiling an app using `toga-iOS` that runs on iOS 26 or newer requires an iOS 26 or newer SDK; the SDK requirement is already enforced in app stores. However, do not use an SDK version of 18 or lower in day-to-day development if you intend to test your app on iOS 26 or newer.

## Installation

`toga-iOS` must be manually installed into an iOS project; The recommended approach for deploying `toga-iOS` is to use [Briefcase](https://briefcase.readthedocs.org) to package your app.

## Implementation details

The `toga-iOS` backend uses the [UIKit Objective-C API](https://developer.apple.com/documentation/uikit).

The native APIs are accessed using [Rubicon Objective-C](https://rubicon-objc.readthedocs.io/).
