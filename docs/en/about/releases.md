# Release History

<!-- rumdl-disable MD024 -->

<!-- towncrier release notes start -->

## 0.5.3 (2025-12-03)

### Features

* Toga now provides a Qt backend for KDE-based desktops. ([#1142](https://github.com/beeware/toga/issues/1142), [#3914](https://github.com/beeware/toga/issues/3914))
* GTK now provides a DateInput widget. ([#1939](https://github.com/beeware/toga/issues/1939))
* Apps can now register a handler that is notified when a window is resized. ([#2304](https://github.com/beeware/toga/issues/2304))
* During application startup, the locale will now be set to match the system's language setting. ([#2773](https://github.com/beeware/toga/issues/2773))
* GTK apps can now detect if the user has expressed a preference to be displayed in dark mode. ([#2841](https://github.com/beeware/toga/issues/2841))
* `Table` and `Tree` widgets on desktop platforms can now accept focus programmatically. ([#2972](https://github.com/beeware/toga/issues/2972))
* The `ActivityIndicator`, `Box`, `Button`, `Canvas`, `DateInput`, `Label` and `TextInput` widgets are now supported with GTK4, along with improved container handling and the added handling of icons. ([#3069](https://github.com/beeware/toga/issues/3069))
* `ListSource.find` now has a `default` parameter which is returned when no match is found. ([#3609](https://github.com/beeware/toga/issues/3609))
* Pack now has a `font` shorthand property for specifying all font properties at once. ([#3631](https://github.com/beeware/toga/issues/3631))
* Toga's web backend now provides deployment configuration information as part of the packaged wheel. This information can be used by tools like Briefcase to control how web content will be rendered. ([#3666](https://github.com/beeware/toga/issues/3666))
* On macOS, if the text for a column doesn't fit in the available space, a tooltip will be shown with the full text. ([#3673](https://github.com/beeware/toga/issues/3673))
* The Android backend now provides an `ActivityIndicator` widget. ([#3729](https://github.com/beeware/toga/issues/3729))
* Support for Python 3.14 was added. ([#3867](https://github.com/beeware/toga/issues/3867))
* macOS and iOS `WebView` widgets now support displaying JavaScript `alert()` and `confirm()` dialogs. ([#3927](https://github.com/beeware/toga/issues/3927))
* GTK `WebView` widgets now support the use of `SharedArrayBuffer` in JavaScript. ([#3927](https://github.com/beeware/toga/issues/3927))

### Bugfixes

* Buttons and other interactive widgets in scroll containers now respond properly to touch events on iOS when scrolled into view. ([#2411](https://github.com/beeware/toga/issues/2411))
* The performance of the `asyncio` event loop on Winforms has been slightly improved. ([#2613](https://github.com/beeware/toga/issues/2613))
* The `NumberInput` widget now uses the correct localization for decimal separators. ([#2773](https://github.com/beeware/toga/issues/2773))
* Deprecation warnings on style handling will no longer be produced when using GTK4 >= 4.10. ([#3069](https://github.com/beeware/toga/issues/3069))
* Toga's Winforms wheel is now correctly tagged to indicate that it is x86_64-specific (as it contains an x86-64 DLL for `WebView` support). ([#3179](https://github.com/beeware/toga/issues/3179))
* Registering a font with a name that shadows a built-in font family name now raises an error instead of falling back to the system font silently. ([#3567](https://github.com/beeware/toga/issues/3567))
* The minimum width hint of the iOS `DateInput` and `TimeInput` widgets will now fit to the actual displayed size of the picker. ([#3580](https://github.com/beeware/toga/issues/3580))
* The `rgb` and `hsl` classes now have a `__str__` that uses modern CSS syntax. For `rgb` this is simply a nice update, but for `hsl` it corrects color rendering issues when using the web backend. ([#3611](https://github.com/beeware/toga/issues/3611))
* On GTK, the scroll position will now be correctly reflected if a `MultilineTextInput` is programmatically scrolled immediately after changing text content. ([#3658](https://github.com/beeware/toga/issues/3658))
* On GTK, mouse drag events are now triggered when modifier keys (e.g. NumLock, Shift) are active. ([#3661](https://github.com/beeware/toga/issues/3661))
* On macOS, the origin of non-primary screens is now correctly calculated when screens are not vertically aligned and the same size. ([#3667](https://github.com/beeware/toga/issues/3667))
* App path attributes were unintentionally made writable in 0.5.2 (e.g. `app.paths.config = <something>` was permitted). This has been fixed. ([#3669](https://github.com/beeware/toga/issues/3669))
* The text of `OptionContainer` tab labels is now guaranteed to be `str` on macOS, instead of an Objective C String. ([#3672](https://github.com/beeware/toga/issues/3672))
* On macOS, pressing Enter or Tab when a row is selected on a table no longer starts row editing mode. ([#3673](https://github.com/beeware/toga/issues/3673))
* Backwards compatibility code in Travertino that allows it to function with pre-0.5 versions of Toga has been made more specific, to prevent it from masking other, unrelated errors. ([#3683](https://github.com/beeware/toga/issues/3683))
* Running a single-file app without an explicit app name under PDB no longer crashes. ([#3686](https://github.com/beeware/toga/issues/3686))
* The interaction between visibility and starting an `ActivityIndicator` on iOS has been resolved. ([#3729](https://github.com/beeware/toga/issues/3729))
* On macOS, the Close and Minimize menu options use the system-provided handlers, ensuring better adherence to system style guides. ([#3775](https://github.com/beeware/toga/issues/3775))
* The show/hide cursor test was made more reliable on Winforms. ([#3783](https://github.com/beeware/toga/issues/3783))
* `OptionContainer` and `ScrollContainer` widgets will now resize continuously during the drag of a parent SplitContainer on macOS. ([#3787](https://github.com/beeware/toga/issues/3787))
* The `toga-demo` app now correctly identifies its icon when run as a Python module. ([#3926](https://github.com/beeware/toga/issues/3926))

### Backward Incompatible Changes

* In order to better match CSS, the `rgb` and `hsl` constructors now silently clip (or in the case of hue, wrap) out-of-range values rather than throwing errors. They also convert them to consistent types: integers for red, blue, green, and hue; and floats for saturation, lightness, and alpha. ([#3611](https://github.com/beeware/toga/issues/3611))
* `rgb` and `hsl` color objects are now read-only; their `r`/`g`/`b`/`a` or `h`/`s`/`l`/`a` attributes can't be altered after creation. Because of this, format conversions (`rgb(...).hsl` or `hsl(...).rgb`) can now cache their results, only performing calculations once. "Converting" a color object to its own type (`rgb(...).rgb` or `hsl(...).hsl`) now returns the original object, rather than a new instance with the same values. ([#3611](https://github.com/beeware/toga/issues/3611))
* Travertino's color-parsing `color()` function interprets hex strings, e.g. `#123`, `#112233`, as well as predefined named colors. Previously, while this was never documented, it also parsed CSS-like declarations like `"rgb(...)"`; this feature has been removed. ([#3611](https://github.com/beeware/toga/issues/3611))
* Previously, Travertino provided an `rgba` and an `hsla` class, as well as `rgb` and `hsl` subclasses that enforce opaque alpha. In order to better match CSS, there is now no difference between these names; the shorter `rgb` and `hsl` are the preferred forms, but `rgba` and `hsla` are direct aliases for them. This can have backwards-incompatible implications; for instance, `rgba(255, 255, 255, .5).rgb` would previously have returned a fully opaque `rgb` instance, while now it will preserve its alpha channel information. ([#3611](https://github.com/beeware/toga/issues/3611))
* Toga (and Travertino) no longer support Python 3.9. ([#3682](https://github.com/beeware/toga/issues/3682))
* If an app provides distribution metadata, the app name will be set based on that metadata, rather than using the app ID or module name as an assumed name. If an app explicitly provides an app ID, the app name will be derived from the last part of an explicitly-provided App ID, rather than being implicitly derived from the module name. ([#3926](https://github.com/beeware/toga/issues/3926))
* Static Positron apps now apply a Cross Origin Opener policy of `same-origin`, and a Cross Origin Embedder Policy of `require-corp`. ([#3927](https://github.com/beeware/toga/issues/3927))

### Documentation

* Toga's documentation was migrated to Markdown format. ([#3719](https://github.com/beeware/toga/issues/3719))

### Misc

* [#3138](https://github.com/beeware/toga/issues/3138), [#3582](https://github.com/beeware/toga/issues/3582), [#3613](https://github.com/beeware/toga/issues/3613), [#3625](https://github.com/beeware/toga/issues/3625), [#3632](https://github.com/beeware/toga/issues/3632), [#3636](https://github.com/beeware/toga/issues/3636), [#3638](https://github.com/beeware/toga/issues/3638), [#3649](https://github.com/beeware/toga/issues/3649), [#3650](https://github.com/beeware/toga/issues/3650), [#3651](https://github.com/beeware/toga/issues/3651), [#3653](https://github.com/beeware/toga/issues/3653), [#3654](https://github.com/beeware/toga/issues/3654), [#3655](https://github.com/beeware/toga/issues/3655), [#3659](https://github.com/beeware/toga/issues/3659), [#3662](https://github.com/beeware/toga/issues/3662), [#3663](https://github.com/beeware/toga/issues/3663), [#3664](https://github.com/beeware/toga/issues/3664), [#3668](https://github.com/beeware/toga/issues/3668), [#3670](https://github.com/beeware/toga/issues/3670), [#3676](https://github.com/beeware/toga/issues/3676), [#3687](https://github.com/beeware/toga/issues/3687), [#3688](https://github.com/beeware/toga/issues/3688), [#3689](https://github.com/beeware/toga/issues/3689), [#3690](https://github.com/beeware/toga/issues/3690), [#3693](https://github.com/beeware/toga/issues/3693), [#3697](https://github.com/beeware/toga/issues/3697), [#3699](https://github.com/beeware/toga/issues/3699), [#3700](https://github.com/beeware/toga/issues/3700), [#3702](https://github.com/beeware/toga/issues/3702), [#3703](https://github.com/beeware/toga/issues/3703), [#3704](https://github.com/beeware/toga/issues/3704), [#3705](https://github.com/beeware/toga/issues/3705), [#3706](https://github.com/beeware/toga/issues/3706), [#3707](https://github.com/beeware/toga/issues/3707), [#3708](https://github.com/beeware/toga/issues/3708), [#3710](https://github.com/beeware/toga/issues/3710), [#3711](https://github.com/beeware/toga/issues/3711), [#3712](https://github.com/beeware/toga/issues/3712), [#3713](https://github.com/beeware/toga/issues/3713), [#3714](https://github.com/beeware/toga/issues/3714), [#3716](https://github.com/beeware/toga/issues/3716), [#3717](https://github.com/beeware/toga/issues/3717), [#3720](https://github.com/beeware/toga/issues/3720), [#3721](https://github.com/beeware/toga/issues/3721), [#3722](https://github.com/beeware/toga/issues/3722), [#3723](https://github.com/beeware/toga/issues/3723), [#3724](https://github.com/beeware/toga/issues/3724), [#3729](https://github.com/beeware/toga/issues/3729), [#3731](https://github.com/beeware/toga/issues/3731), [#3735](https://github.com/beeware/toga/issues/3735), [#3736](https://github.com/beeware/toga/issues/3736), [#3737](https://github.com/beeware/toga/issues/3737), [#3738](https://github.com/beeware/toga/issues/3738), [#3739](https://github.com/beeware/toga/issues/3739), [#3740](https://github.com/beeware/toga/issues/3740), [#3741](https://github.com/beeware/toga/issues/3741), [#3742](https://github.com/beeware/toga/issues/3742), [#3744](https://github.com/beeware/toga/issues/3744), [#3754](https://github.com/beeware/toga/issues/3754), [#3755](https://github.com/beeware/toga/issues/3755), [#3756](https://github.com/beeware/toga/issues/3756), [#3757](https://github.com/beeware/toga/issues/3757), [#3758](https://github.com/beeware/toga/issues/3758), [#3761](https://github.com/beeware/toga/issues/3761), [#3764](https://github.com/beeware/toga/issues/3764), [#3765](https://github.com/beeware/toga/issues/3765), [#3766](https://github.com/beeware/toga/issues/3766), [#3770](https://github.com/beeware/toga/issues/3770), [#3771](https://github.com/beeware/toga/issues/3771), [#3772](https://github.com/beeware/toga/issues/3772), [#3776](https://github.com/beeware/toga/issues/3776), [#3784](https://github.com/beeware/toga/issues/3784), [#3789](https://github.com/beeware/toga/issues/3789), [#3790](https://github.com/beeware/toga/issues/3790), [#3795](https://github.com/beeware/toga/issues/3795), [#3796](https://github.com/beeware/toga/issues/3796), [#3797](https://github.com/beeware/toga/issues/3797), [#3798](https://github.com/beeware/toga/issues/3798), [#3799](https://github.com/beeware/toga/issues/3799), [#3800](https://github.com/beeware/toga/issues/3800), [#3801](https://github.com/beeware/toga/issues/3801), [#3802](https://github.com/beeware/toga/issues/3802), [#3803](https://github.com/beeware/toga/issues/3803), [#3804](https://github.com/beeware/toga/issues/3804), [#3805](https://github.com/beeware/toga/issues/3805), [#3806](https://github.com/beeware/toga/issues/3806), [#3807](https://github.com/beeware/toga/issues/3807), [#3808](https://github.com/beeware/toga/issues/3808), [#3809](https://github.com/beeware/toga/issues/3809), [#3810](https://github.com/beeware/toga/issues/3810), [#3811](https://github.com/beeware/toga/issues/3811), [#3812](https://github.com/beeware/toga/issues/3812), [#3813](https://github.com/beeware/toga/issues/3813), [#3814](https://github.com/beeware/toga/issues/3814), [#3815](https://github.com/beeware/toga/issues/3815), [#3816](https://github.com/beeware/toga/issues/3816), [#3817](https://github.com/beeware/toga/issues/3817), [#3818](https://github.com/beeware/toga/issues/3818), [#3821](https://github.com/beeware/toga/issues/3821), [#3821](https://github.com/beeware/toga/issues/3821), [#3824](https://github.com/beeware/toga/issues/3824), [#3825](https://github.com/beeware/toga/issues/3825), [#3826](https://github.com/beeware/toga/issues/3826), [#3827](https://github.com/beeware/toga/issues/3827), [#3828](https://github.com/beeware/toga/issues/3828), [#3829](https://github.com/beeware/toga/issues/3829), [#3830](https://github.com/beeware/toga/issues/3830), [#3831](https://github.com/beeware/toga/issues/3831), [#3833](https://github.com/beeware/toga/issues/3833), [#3836](https://github.com/beeware/toga/issues/3836), [#3837](https://github.com/beeware/toga/issues/3837), [#3840](https://github.com/beeware/toga/issues/3840), [#3841](https://github.com/beeware/toga/issues/3841), [#3842](https://github.com/beeware/toga/issues/3842), [#3843](https://github.com/beeware/toga/issues/3843), [#3844](https://github.com/beeware/toga/issues/3844), [#3845](https://github.com/beeware/toga/issues/3845), [#3846](https://github.com/beeware/toga/issues/3846), [#3847](https://github.com/beeware/toga/issues/3847), [#3848](https://github.com/beeware/toga/issues/3848), [#3849](https://github.com/beeware/toga/issues/3849), [#3850](https://github.com/beeware/toga/issues/3850), [#3851](https://github.com/beeware/toga/issues/3851), [#3852](https://github.com/beeware/toga/issues/3852), [#3853](https://github.com/beeware/toga/issues/3853), [#3855](https://github.com/beeware/toga/issues/3855), [#3856](https://github.com/beeware/toga/issues/3856), [#3858](https://github.com/beeware/toga/issues/3858), [#3860](https://github.com/beeware/toga/issues/3860), [#3864](https://github.com/beeware/toga/issues/3864), [#3865](https://github.com/beeware/toga/issues/3865), [#3866](https://github.com/beeware/toga/issues/3866), [#3874](https://github.com/beeware/toga/issues/3874), [#3875](https://github.com/beeware/toga/issues/3875), [#3876](https://github.com/beeware/toga/issues/3876), [#3877](https://github.com/beeware/toga/issues/3877), [#3878](https://github.com/beeware/toga/issues/3878), [#3879](https://github.com/beeware/toga/issues/3879), [#3880](https://github.com/beeware/toga/issues/3880), [#3882](https://github.com/beeware/toga/issues/3882), [#3883](https://github.com/beeware/toga/issues/3883), [#3884](https://github.com/beeware/toga/issues/3884), [#3885](https://github.com/beeware/toga/issues/3885), [#3887](https://github.com/beeware/toga/issues/3887), [#3892](https://github.com/beeware/toga/issues/3892), [#3893](https://github.com/beeware/toga/issues/3893), [#3894](https://github.com/beeware/toga/issues/3894), [#3895](https://github.com/beeware/toga/issues/3895), [#3898](https://github.com/beeware/toga/issues/3898), [#3899](https://github.com/beeware/toga/issues/3899), [#3902](https://github.com/beeware/toga/issues/3902), [#3908](https://github.com/beeware/toga/issues/3908), [#3909](https://github.com/beeware/toga/issues/3909), [#3910](https://github.com/beeware/toga/issues/3910), [#3911](https://github.com/beeware/toga/issues/3911), [#3912](https://github.com/beeware/toga/issues/3912), [#3913](https://github.com/beeware/toga/issues/3913), [#3933](https://github.com/beeware/toga/issues/3933), [#3934](https://github.com/beeware/toga/issues/3934), [#3936](https://github.com/beeware/toga/issues/3936), [#3937](https://github.com/beeware/toga/issues/3937), [#3938](https://github.com/beeware/toga/issues/3938), [#3940](https://github.com/beeware/toga/issues/3940)

## 0.5.2 (2025-07-10)

### Features

- iOS and macOS backends now provide DateInput and TimeInput widgets. ([#1939](https://github.com/beeware/toga/issues/1939))
- The Android backend can now identify if dark mode is enabled. ([#2841](https://github.com/beeware/toga/issues/2841))
- Toga now has a layout debugging mode. If you set `TOGA_DEBUG_LAYOUT=1` in your app's runtime environment or `toga.Widget.DEBUG_LAYOUT_ENABLED == True` directly in the app's code, widgets will be rendered with different background colors, making it easier to identify how space is being allocated by Toga's layout algorithm. ([#2953](https://github.com/beeware/toga/issues/2953))
- `toga.App.paths` properties now create the path on demand, if it does not already exist. ([#3236](https://github.com/beeware/toga/issues/3236))
- The Web backend now provides Selection and Slider widgets. ([#3334](https://github.com/beeware/toga/issues/3334))
- Lazily loaded objects in the `toga` namespace now support type checking. ([#3358](https://github.com/beeware/toga/issues/3358))
- Winforms now provides an ActivityIndicator widget. ([#3473](https://github.com/beeware/toga/issues/3473))
- WebViews on macOS now support file uploads. ([#3484](https://github.com/beeware/toga/issues/3484))
- `Pack.font_family` now accepts a list of possible values; text will be rendered with the first font family that is available. ([#3526](https://github.com/beeware/toga/issues/3526))
- App paths are now cached upon first retrieval. ([#3544](https://github.com/beeware/toga/issues/3544))
- On Windows and GTK, Toga now supports loading arbitrary fronts from the user's system, in addition to Toga's predefined set of system fonts and any that you have registered. (This was already possible on Windows, but undocumented.) ([#3569](https://github.com/beeware/toga/issues/3569))
- On GTK, a document-based app with multiple file extensions registered will now provide a file type filter that will match all available document types. ([#3570](https://github.com/beeware/toga/issues/3570))

### Bugfixes

- Attempting to refresh a window with no content no longer raises an error on Textual. ([#2818](https://github.com/beeware/toga/issues/2818))
- MultilineTextInput widget will no longer fire `on_change` events during creation on Windows. ([#3290](https://github.com/beeware/toga/issues/3290))
- The Textual backend no longer raises superfluous console messages when the app shuts down. ([#3399](https://github.com/beeware/toga/issues/3399))
- Apps that use a function-based app startup method now validate that the startup method returns content that can be added to the main window. ([#3444](https://github.com/beeware/toga/issues/3444))
- Buttons in Toga Web now correctly respond to clicks and trigger their associated actions. ([#3451](https://github.com/beeware/toga/issues/3451))
- Table Widget on Windows now only fires one event on item selection. ([#3472](https://github.com/beeware/toga/issues/3472))
- Older Linux distributions (such as Ubuntu 22.04) that ship with GLib \< 2.74 can now use GTK4 with Toga. ([#3525](https://github.com/beeware/toga/issues/3525))
- ([#3531](https://github.com/beeware/toga/issues/3531))
- On macOS, `MultilineTextInput` will no longer automatically convert straight quotes to smart quotes. ([#3546](https://github.com/beeware/toga/issues/3546))
- A crash on Android 9 (and earlier) caused by a symbol that wasn't available on those versions has been resolved. ([#3554](https://github.com/beeware/toga/issues/3554))
- On macOS, document-based apps no longer raise an error on startup about the event loop already running. ([#3570](https://github.com/beeware/toga/issues/3570))
- When an app has no windows, GTK no longer returns an error when requesting `toga.App.current_window`. ([#3570](https://github.com/beeware/toga/issues/3570))
- The conversion of HSL values with a hue between 240 and 330 has been corrected. The previous calculation reversed the red and green components of the converted colors. ([#3584](https://github.com/beeware/toga/issues/3584))

### Backward Incompatible Changes

- `toga.Font` objects now raise an *UnknownFontError* instead of silently falling back to system font if the font family can't be successfully loaded. ([#3526](https://github.com/beeware/toga/issues/3526))

### Documentation

- Documentation for installing platform-specific dependencies has been improved. ([#1688](https://github.com/beeware/toga/issues/1688))
- Toga's documentation now uses a header and style consistent with the BeeWare website. ([#3538](https://github.com/beeware/toga/issues/3538))
- A topic guide on managing file paths has been added. ([#3552](https://github.com/beeware/toga/issues/3552))

### Misc

- [#2453](https://github.com/beeware/toga/issues/2453), [#2975](https://github.com/beeware/toga/issues/2975), [#3138](https://github.com/beeware/toga/issues/3138), [#3420](https://github.com/beeware/toga/issues/3420), [#3426](https://github.com/beeware/toga/issues/3426), [#3427](https://github.com/beeware/toga/issues/3427), [#3428](https://github.com/beeware/toga/issues/3428), [#3429](https://github.com/beeware/toga/issues/3429), [#3430](https://github.com/beeware/toga/issues/3430), [#3431](https://github.com/beeware/toga/issues/3431), [#3432](https://github.com/beeware/toga/issues/3432), [#3433](https://github.com/beeware/toga/issues/3433), [#3434](https://github.com/beeware/toga/issues/3434), [#3435](https://github.com/beeware/toga/issues/3435), [#3436](https://github.com/beeware/toga/issues/3436), [#3437](https://github.com/beeware/toga/issues/3437), [#3438](https://github.com/beeware/toga/issues/3438), [#3439](https://github.com/beeware/toga/issues/3439), [#3441](https://github.com/beeware/toga/issues/3441), [#3444](https://github.com/beeware/toga/issues/3444), [#3447](https://github.com/beeware/toga/issues/3447), [#3452](https://github.com/beeware/toga/issues/3452), [#3453](https://github.com/beeware/toga/issues/3453), [#3454](https://github.com/beeware/toga/issues/3454), [#3455](https://github.com/beeware/toga/issues/3455), [#3456](https://github.com/beeware/toga/issues/3456), [#3457](https://github.com/beeware/toga/issues/3457), [#3458](https://github.com/beeware/toga/issues/3458), [#3459](https://github.com/beeware/toga/issues/3459), [#3460](https://github.com/beeware/toga/issues/3460), [#3461](https://github.com/beeware/toga/issues/3461), [#3462](https://github.com/beeware/toga/issues/3462), [#3463](https://github.com/beeware/toga/issues/3463), [#3464](https://github.com/beeware/toga/issues/3464), [#3465](https://github.com/beeware/toga/issues/3465), [#3486](https://github.com/beeware/toga/issues/3486), [#3488](https://github.com/beeware/toga/issues/3488), [#3489](https://github.com/beeware/toga/issues/3489), [#3490](https://github.com/beeware/toga/issues/3490), [#3491](https://github.com/beeware/toga/issues/3491), [#3492](https://github.com/beeware/toga/issues/3492), [#3493](https://github.com/beeware/toga/issues/3493), [#3494](https://github.com/beeware/toga/issues/3494), [#3495](https://github.com/beeware/toga/issues/3495), [#3496](https://github.com/beeware/toga/issues/3496), [#3497](https://github.com/beeware/toga/issues/3497), [#3498](https://github.com/beeware/toga/issues/3498), [#3499](https://github.com/beeware/toga/issues/3499), [#3500](https://github.com/beeware/toga/issues/3500), [#3501](https://github.com/beeware/toga/issues/3501), [#3509](https://github.com/beeware/toga/issues/3509), [#3511](https://github.com/beeware/toga/issues/3511), [#3512](https://github.com/beeware/toga/issues/3512), [#3513](https://github.com/beeware/toga/issues/3513), [#3514](https://github.com/beeware/toga/issues/3514), [#3515](https://github.com/beeware/toga/issues/3515), [#3516](https://github.com/beeware/toga/issues/3516), [#3517](https://github.com/beeware/toga/issues/3517), [#3518](https://github.com/beeware/toga/issues/3518), [#3519](https://github.com/beeware/toga/issues/3519), [#3520](https://github.com/beeware/toga/issues/3520), [#3521](https://github.com/beeware/toga/issues/3521), [#3522](https://github.com/beeware/toga/issues/3522), [#3523](https://github.com/beeware/toga/issues/3523), [#3528](https://github.com/beeware/toga/issues/3528), [#3533](https://github.com/beeware/toga/issues/3533), [#3539](https://github.com/beeware/toga/issues/3539), [#3540](https://github.com/beeware/toga/issues/3540), [#3541](https://github.com/beeware/toga/issues/3541), [#3542](https://github.com/beeware/toga/issues/3542), [#3550](https://github.com/beeware/toga/issues/3550), [#3556](https://github.com/beeware/toga/issues/3556), [#3557](https://github.com/beeware/toga/issues/3557), [#3558](https://github.com/beeware/toga/issues/3558), [#3559](https://github.com/beeware/toga/issues/3559), [#3560](https://github.com/beeware/toga/issues/3560), [#3561](https://github.com/beeware/toga/issues/3561), [#3562](https://github.com/beeware/toga/issues/3562), [#3563](https://github.com/beeware/toga/issues/3563), [#3569](https://github.com/beeware/toga/issues/3569), [#3572](https://github.com/beeware/toga/issues/3572), [#3575](https://github.com/beeware/toga/issues/3575), [#3576](https://github.com/beeware/toga/issues/3576), [#3577](https://github.com/beeware/toga/issues/3577), [#3578](https://github.com/beeware/toga/issues/3578), [#3579](https://github.com/beeware/toga/issues/3579), [#3583](https://github.com/beeware/toga/issues/3583), [#3586](https://github.com/beeware/toga/issues/3586), [#3587](https://github.com/beeware/toga/issues/3587), [#3587](https://github.com/beeware/toga/issues/3587), [#3588](https://github.com/beeware/toga/issues/3588), [#3589](https://github.com/beeware/toga/issues/3589), [#3591](https://github.com/beeware/toga/issues/3591), [#3592](https://github.com/beeware/toga/issues/3592), [#3593](https://github.com/beeware/toga/issues/3593), [#3594](https://github.com/beeware/toga/issues/3594), [#3595](https://github.com/beeware/toga/issues/3595), [#3601](https://github.com/beeware/toga/issues/3601), [#3603](https://github.com/beeware/toga/issues/3603), [#3604](https://github.com/beeware/toga/issues/3604), [#3605](https://github.com/beeware/toga/issues/3605), [#3607](https://github.com/beeware/toga/issues/3607), [#3608](https://github.com/beeware/toga/issues/3608), [#3617](https://github.com/beeware/toga/issues/3617), [#3618](https://github.com/beeware/toga/issues/3618), [#3619](https://github.com/beeware/toga/issues/3619), [#3620](https://github.com/beeware/toga/issues/3620), [#3621](https://github.com/beeware/toga/issues/3621), [#3622](https://github.com/beeware/toga/issues/3622), [#3623](https://github.com/beeware/toga/issues/3623), [#3629](https://github.com/beeware/toga/issues/3629), [#3633](https://github.com/beeware/toga/issues/3633)

## 0.5.1 (2025-05-08)

### Features

- The WebView widget now supports specifying static content on instantiation. ([#2851](https://github.com/beeware/toga/issues/2851))
- The content of a WebView can now be assigned using the *content* property, without providing a root URL for the content. ([#2854](https://github.com/beeware/toga/issues/2854))
- Application of style properties has been streamlined to reduce redundant font creation and widget-refreshing. ([#3273](https://github.com/beeware/toga/issues/3273))
- The Canvas example app's UI controls have been reorganized and more clearly labeled. ([#3321](https://github.com/beeware/toga/issues/3321))
- The Web backend now supports the DateInput, ScrollContainer and TimeInput widgets. ([#3334](https://github.com/beeware/toga/issues/3334))

### Bugfixes

- The asyncio event loop used on Winforms now shuts down correctly, ensuring there are no dangling resources on application exit. ([#3266](https://github.com/beeware/toga/issues/3266))
- Changing a widget's `text_direction` now triggers a layout refresh, since it can affect child positioning. ([#3268](https://github.com/beeware/toga/issues/3268))
- Table rows are now highlighted on Winforms when the widget doesn't have focus. ([#3269](https://github.com/beeware/toga/issues/3269))
- Support for GTK3 installs that use a GIO release older than 2.72 has been restored. Ubuntu 22.04, and other Debian 12-derived systems are affected by this issue. ([#3296](https://github.com/beeware/toga/issues/3296))
- Some errors observed on the Web backend during app startup have been resolved. ([#3301](https://github.com/beeware/toga/issues/3301))
- An incompatibility with Textual 3.0 that caused log messages to be generated on the console on app exit has been resolved. ([#3342](https://github.com/beeware/toga/issues/3342))
- Window visibility and focus events in the web backend no longer raise errors when the browser window loses focus ([#3345](https://github.com/beeware/toga/issues/3345))
- A crash caused by the `name` argument added to asynchronous tasks in Python 3.13.3 has been corrected. ([#3394](https://github.com/beeware/toga/issues/3394))
- The type annotation for directional style properties (`margin`, and the deprecated `padding` alias) has been corrected. ([#3396](https://github.com/beeware/toga/issues/3396))

### Backward Incompatible Changes

- Supplying multiple arguments to `BaseStyle.apply()` (and therefore `Pack.apply()`) has been deprecated. If you want to apply multiple arguments at once, apply them within the `with style_object.batch_apply()` context manager. ([#3273](https://github.com/beeware/toga/issues/3273))
- The `anticlockwise` parameter to the Canvas drawing context's `arc` and `ellipse` methods (and the `Arc` and `Ellipse` drawing objects) has been deprecated; use `counterclockwise` instead. ([#3300](https://github.com/beeware/toga/issues/3300))

### Misc

- [#3261](https://github.com/beeware/toga/issues/3261), [#3262](https://github.com/beeware/toga/issues/3262), [#3263](https://github.com/beeware/toga/issues/3263), [#3267](https://github.com/beeware/toga/issues/3267), [#3272](https://github.com/beeware/toga/issues/3272), [#3275](https://github.com/beeware/toga/issues/3275), [#3277](https://github.com/beeware/toga/issues/3277), [#3278](https://github.com/beeware/toga/issues/3278), [#3279](https://github.com/beeware/toga/issues/3279), [#3280](https://github.com/beeware/toga/issues/3280), [#3281](https://github.com/beeware/toga/issues/3281), [#3283](https://github.com/beeware/toga/issues/3283), [#3284](https://github.com/beeware/toga/issues/3284), [#3288](https://github.com/beeware/toga/issues/3288), [#3289](https://github.com/beeware/toga/issues/3289), [#3291](https://github.com/beeware/toga/issues/3291), [#3292](https://github.com/beeware/toga/issues/3292), [#3294](https://github.com/beeware/toga/issues/3294), [#3302](https://github.com/beeware/toga/issues/3302), [#3303](https://github.com/beeware/toga/issues/3303), [#3304](https://github.com/beeware/toga/issues/3304), [#3305](https://github.com/beeware/toga/issues/3305), [#3306](https://github.com/beeware/toga/issues/3306), [#3307](https://github.com/beeware/toga/issues/3307), [#3308](https://github.com/beeware/toga/issues/3308), [#3309](https://github.com/beeware/toga/issues/3309), [#3310](https://github.com/beeware/toga/issues/3310), [#3311](https://github.com/beeware/toga/issues/3311), [#3312](https://github.com/beeware/toga/issues/3312), [#3313](https://github.com/beeware/toga/issues/3313), [#3314](https://github.com/beeware/toga/issues/3314), [#3315](https://github.com/beeware/toga/issues/3315), [#3316](https://github.com/beeware/toga/issues/3316), [#3317](https://github.com/beeware/toga/issues/3317), [#3318](https://github.com/beeware/toga/issues/3318), [#3319](https://github.com/beeware/toga/issues/3319), [#3320](https://github.com/beeware/toga/issues/3320), [#3331](https://github.com/beeware/toga/issues/3331), [#3332](https://github.com/beeware/toga/issues/3332), [#3336](https://github.com/beeware/toga/issues/3336), [#3341](https://github.com/beeware/toga/issues/3341), [#3342](https://github.com/beeware/toga/issues/3342), [#3346](https://github.com/beeware/toga/issues/3346), [#3347](https://github.com/beeware/toga/issues/3347), [#3348](https://github.com/beeware/toga/issues/3348), [#3349](https://github.com/beeware/toga/issues/3349), [#3350](https://github.com/beeware/toga/issues/3350), [#3351](https://github.com/beeware/toga/issues/3351), [#3352](https://github.com/beeware/toga/issues/3352), [#3353](https://github.com/beeware/toga/issues/3353), [#3354](https://github.com/beeware/toga/issues/3354), [#3355](https://github.com/beeware/toga/issues/3355), [#3356](https://github.com/beeware/toga/issues/3356), [#3357](https://github.com/beeware/toga/issues/3357), [#3363](https://github.com/beeware/toga/issues/3363), [#3364](https://github.com/beeware/toga/issues/3364), [#3365](https://github.com/beeware/toga/issues/3365), [#3366](https://github.com/beeware/toga/issues/3366), [#3367](https://github.com/beeware/toga/issues/3367), [#3368](https://github.com/beeware/toga/issues/3368), [#3369](https://github.com/beeware/toga/issues/3369), [#3370](https://github.com/beeware/toga/issues/3370), [#3371](https://github.com/beeware/toga/issues/3371), [#3372](https://github.com/beeware/toga/issues/3372), [#3373](https://github.com/beeware/toga/issues/3373), [#3374](https://github.com/beeware/toga/issues/3374), [#3375](https://github.com/beeware/toga/issues/3375), [#3376](https://github.com/beeware/toga/issues/3376), [#3377](https://github.com/beeware/toga/issues/3377), [#3378](https://github.com/beeware/toga/issues/3378), [#3379](https://github.com/beeware/toga/issues/3379), [#3380](https://github.com/beeware/toga/issues/3380), [#3381](https://github.com/beeware/toga/issues/3381), [#3382](https://github.com/beeware/toga/issues/3382), [#3383](https://github.com/beeware/toga/issues/3383), [#3384](https://github.com/beeware/toga/issues/3384), [#3385](https://github.com/beeware/toga/issues/3385), [#3386](https://github.com/beeware/toga/issues/3386), [#3404](https://github.com/beeware/toga/issues/3404), [#3406](https://github.com/beeware/toga/issues/3406), [#3407](https://github.com/beeware/toga/issues/3407), [#3408](https://github.com/beeware/toga/issues/3408), [#3409](https://github.com/beeware/toga/issues/3409), [#3410](https://github.com/beeware/toga/issues/3410), [#3411](https://github.com/beeware/toga/issues/3411), [#3412](https://github.com/beeware/toga/issues/3412), [#3413](https://github.com/beeware/toga/issues/3413), [#3414](https://github.com/beeware/toga/issues/3414), [#3415](https://github.com/beeware/toga/issues/3415), [#3416](https://github.com/beeware/toga/issues/3416), [#3417](https://github.com/beeware/toga/issues/3417), [#3418](https://github.com/beeware/toga/issues/3418), [#3419](https://github.com/beeware/toga/issues/3419)

## 0.5.0 (2025-03-14)

### Features

- A `justify_content` style attribute has been added, which aligns children along a box's main axis. ([#1194](https://github.com/beeware/toga/issues/1194))
- Toga apps can now detect and set their window states including maximized, minimized, normal, full screen and presentation states. ([#1857](https://github.com/beeware/toga/issues/1857))
- A `gap` style attribute has been added, which adds space between adjacent children of a box. ([#1943](https://github.com/beeware/toga/issues/1943))
- Windows can now respond to changes in focus and visibility. ([#2009](https://github.com/beeware/toga/issues/2009))
- The line height of multi-line text on a Canvas can now be configured. ([#2144](https://github.com/beeware/toga/issues/2144))
- Apps can now interrogate whether they are in dark mode on some platforms. ([#2841](https://github.com/beeware/toga/issues/2841))
- Toga GTK now supports location services via integration with GeoClue and the XDG Location Portal. ([#2990](https://github.com/beeware/toga/issues/2990))
- Android cameras now describe themselves in terms of the direction they are facing (if known). ([#2996](https://github.com/beeware/toga/issues/2996))
- `toga.Row` and `toga.Column` can now be used as a shorthand for `toga.Box(style=Pack(direction=...))`. ([#3010](https://github.com/beeware/toga/issues/3010))
- Style properties can now be passed directly to a widget's constructor, or accessed as attributes, without explicitly using a `style` object. ([#3011](https://github.com/beeware/toga/issues/3011))
- The `Pack.margin` property (and its deprecated alias, `padding`) can now be accessed via bracket notation, as in `style["margin"]`. (Previously this worked for the "sub-properties" of `margin_top` etc., but not for `margin`/`padding` itself.) ([#3044](https://github.com/beeware/toga/issues/3044))
- The `WebView` widget now supports the retrieval of cookies. ([#3068](https://github.com/beeware/toga/issues/3068))
- The Travertino library, providing the base classes for Toga's style and box model, is now managed as part of the Toga release process. ([#3086](https://github.com/beeware/toga/issues/3086))
- Initial experimental support for GTK4 has been added to Toga's GTK backend. This support can be enabled by setting `TOGA_GTK=4` in your environment. ([#3087](https://github.com/beeware/toga/issues/3087))
- The `align_items` and `justify_content` properties now have the aliases `horizontal_align_items`, `vertical_align_items`, `horizontal_align_content` and `vertical_align_content` that explicitly describe layout behavior in the named direction. ([#3111](https://github.com/beeware/toga/issues/3111))
- A Briefcase bootstrap for generating Positron apps (i.e., apps that are a web view in a native wrapper - Electron, but more positive, because it's Python) was added. ([#3114](https://github.com/beeware/toga/issues/3114))
- The Travertino library now has 100% test coverage. ([#3129](https://github.com/beeware/toga/issues/3129))
- The Travertino library now includes APIs to perform alpha blending operations and conversion of RGBA to HSLA color representations. ([#3140](https://github.com/beeware/toga/issues/3140))
- Travertino now has an `aliased_property` descriptor to support declaration of property name aliases in styles. ([#3213](https://github.com/beeware/toga/issues/3213))
- The Pack style representation is now a dataclass. This should allow most IDEs to infer the names and types of properties and suggest them in creating a Pack instance. ([#3215](https://github.com/beeware/toga/issues/3215))

### Bugfixes

- On WinForms, Box, Canvas, Label and ImageView widgets now have transparent backgrounds by default. ([#767](https://github.com/beeware/toga/issues/767))
- On iOS, Box, Canvas, ImageView, Label, ProgressBar, ScrollContainer and Slider widgets now have transparent backgrounds by default. ([#767](https://github.com/beeware/toga/issues/767))
- DPI scaling on Windows has been improved, fixing a number of resolution and scaling issues. ([#2155](https://github.com/beeware/toga/issues/2155))
- On WinForms, the background color of a widget now correctly honors the alpha channel of the selected color. ([#2425](https://github.com/beeware/toga/issues/2425))
- If a WebView widget completes navigation to a new URL while it is being destroyed, an error is no longer raised on macOS or iOS. ([#2512](https://github.com/beeware/toga/issues/2512))
- Widgets on the iOS backend no longer leak memory when destroyed. ([#2849](https://github.com/beeware/toga/issues/2849))
- On macOS, when a dialog is in focus, `App.current_window` now returns the host window, instead of raising an `AttributeError`. ([#2926](https://github.com/beeware/toga/issues/2926))
- An issue with creating dialogs on the Textual backend was resolved. ([#2949](https://github.com/beeware/toga/issues/2949))
- A newly added, visible widget will be hidden when added to a widget hierarchy where an ancestor is hidden. ([#2950](https://github.com/beeware/toga/issues/2950))
- Multi-letter keyboard navigation in Tables and DetailedLists with the WinForms backend is now functional. ([#2956](https://github.com/beeware/toga/issues/2956))
- The web backend now uses the Shoelace default font in all browsers. ([#3035](https://github.com/beeware/toga/issues/3035))
- The `hardware` example app now correctly demonstrates usage of the location services method `current_location`. ([#3045](https://github.com/beeware/toga/issues/3045))
- On GTK, when a window is hidden, the `window.state` getter now correctly reports the state when the window was last visible. ([#3105](https://github.com/beeware/toga/issues/3105))
- On Android, setting a custom background color on widgets now preserves the native look and feel. ([#3118](https://github.com/beeware/toga/issues/3118))
- On Android, setting widget background color to `TRANSPARENT` now correctly sets it to transparent. ([#3118](https://github.com/beeware/toga/issues/3118))
- The binary dependencies for the GTK backend have been updated to reflect changes in requirements of PyGObject. ([#3143](https://github.com/beeware/toga/issues/3143))
- On Android, `DetailedList` and `Table` widgets now correctly unset the highlight color when a row is deselected. ([#3156](https://github.com/beeware/toga/issues/3156))
- ([#3163](https://github.com/beeware/toga/issues/3163))

### Backward Incompatible Changes

- "Full screen mode" on an app has been renamed "Presentation mode" to avoid the ambiguity with "full screen mode" on a window. The `toga.App.enter_full_screen` and `toga.App.exit_full_screen` APIs have been renamed `toga.App.enter_presentation_mode` and `toga.App.exit_presentation_mode`, respectively. ([#1857](https://github.com/beeware/toga/issues/1857))
- The use of generators as event handlers has been deprecated. Any generator-based event handler can be converted into an asynchronous co-routine by converting the handler to `async def`, and using `await asyncio.sleep(t)` in place of `yield t` (for some sleep interval `t`). ([#2721](https://github.com/beeware/toga/issues/2721))
- Widgets now create and return their implementations via a `_create()` method. A user-created custom widget that inherits from an existing Toga widget and uses the same implementation will require no changes. Any user-created widgets that need to specify their own implementation should do so in `_create()` and return that implementation. Existing user code inheriting from `Widget` that assigns its implementation before calling `super().__init__()` will continue to function, but give a `RuntimeWarning`; unfortunately, this change breaks any existing code that doesn't create its implementation until afterward. Such usage will now raise an exception. ([#2942](https://github.com/beeware/toga/issues/2942))
- Pack's `padding` and `alignment` properties have been renamed to `margin` and `align_items`, to match their CSS analogues. `align_items` also now takes CSS-compatible values of `START`, `CENTER`, and `END`, instead of `alignment`'s `TOP`/`RIGHT`/`BOTTOM`/`LEFT`/`CENTER`. The old names are still present — and `alignment` still takes its existing values — but these constants are deprecated. ([#3033](https://github.com/beeware/toga/issues/3033))
- APIs marked as deprecated in Toga 0.4.0 and earlier have been removed. ([#3059](https://github.com/beeware/toga/issues/3059))
- The `show()` and `hide()` APIs can no longer be used on a window while it is in a `MINIMIZED`, `FULLSCREEN` or `PRESENTATION` state. ([#3109](https://github.com/beeware/toga/issues/3109))
- If window size is unchanged as a result of a resize request, a layout of window content is no longer triggered. ([#3131](https://github.com/beeware/toga/issues/3131))
- If you're running on Ubuntu 22.04, Debian 11 or Debian 12, you'll need to manually add a pin for `PyGObject==3.50.0` to your project. This is because recent PyGObject releases specify a requirement on `girepository-2.0`, which is not available on older Debian-based distributions. A manual pin is required because there's no way to express a dependency on a system package as part of Python's requirements specifications. ([#3143](https://github.com/beeware/toga/issues/3143))
- The signature of the `apply` method of `BaseStyle` (and thus `Pack`) has changed. Rather than taking a property name and value, it now takes only the name, and the style object checks its own current value for that property to know what to apply. This method is normally used internally, but any user code calling it manually will get a `DeprecationWarning` if it supplies two arguments. ([#3159](https://github.com/beeware/toga/issues/3159))
- Travertino's `BaseStyle.reapply()` (and thus Toga's `Pack.reapply()`) has been deprecated; the correct usage is now to call `.apply()` with no arguments. User code is unlikely to ever call this method, but Toga releases before (and including) 0.4.8 calls it extensively, so users who update Travertino but not Toga will receive a `DeprecationWarning`. ([#3160](https://github.com/beeware/toga/issues/3160))
- Travertino's `declaration` module has been split into two smaller modules, `properties` and `style`. Toga's imports have been updated to the new locations, but users with Toga \<= 0.4.8 that update Travertino to 0.5.0 (and anyone who may be accessing these classes in user code) will get a `DeprecationWarning` explaining the situation. ([#3195](https://github.com/beeware/toga/issues/3195))

### Documentation

- Tutorial 3 was extended to explain limitations of the browser example, and suggest some extension activities. ([#2998](https://github.com/beeware/toga/issues/2998))
- A summary of Toga's API design principles has been added. ([#3170](https://github.com/beeware/toga/issues/3170))
- Widget screenshots have been added for the Web backend. ([#3259](https://github.com/beeware/toga/issues/3259))

### Misc

- [#2547](https://github.com/beeware/toga/issues/2547), [#2893](https://github.com/beeware/toga/issues/2893), [#2920](https://github.com/beeware/toga/issues/2920), [#2921](https://github.com/beeware/toga/issues/2921), [#2922](https://github.com/beeware/toga/issues/2922), [#2923](https://github.com/beeware/toga/issues/2923), [#2925](https://github.com/beeware/toga/issues/2925), [#2931](https://github.com/beeware/toga/issues/2931), [#2932](https://github.com/beeware/toga/issues/2932), [#2933](https://github.com/beeware/toga/issues/2933), [#2934](https://github.com/beeware/toga/issues/2934), [#2935](https://github.com/beeware/toga/issues/2935), [#2936](https://github.com/beeware/toga/issues/2936), [#2939](https://github.com/beeware/toga/issues/2939), [#2941](https://github.com/beeware/toga/issues/2941), [#2942](https://github.com/beeware/toga/issues/2942), [#2951](https://github.com/beeware/toga/issues/2951), [#2954](https://github.com/beeware/toga/issues/2954), [#2965](https://github.com/beeware/toga/issues/2965), [#2967](https://github.com/beeware/toga/issues/2967), [#2968](https://github.com/beeware/toga/issues/2968), [#2970](https://github.com/beeware/toga/issues/2970), [#2975](https://github.com/beeware/toga/issues/2975), [#2976](https://github.com/beeware/toga/issues/2976), [#2978](https://github.com/beeware/toga/issues/2978), [#2980](https://github.com/beeware/toga/issues/2980), [#2981](https://github.com/beeware/toga/issues/2981), [#2982](https://github.com/beeware/toga/issues/2982), [#2983](https://github.com/beeware/toga/issues/2983), [#2984](https://github.com/beeware/toga/issues/2984), [#2985](https://github.com/beeware/toga/issues/2985), [#2986](https://github.com/beeware/toga/issues/2986), [#2987](https://github.com/beeware/toga/issues/2987), [#2988](https://github.com/beeware/toga/issues/2988), [#2989](https://github.com/beeware/toga/issues/2989), [#2991](https://github.com/beeware/toga/issues/2991), [#2997](https://github.com/beeware/toga/issues/2997), [#3006](https://github.com/beeware/toga/issues/3006), [#3007](https://github.com/beeware/toga/issues/3007), [#3008](https://github.com/beeware/toga/issues/3008), [#3016](https://github.com/beeware/toga/issues/3016), [#3020](https://github.com/beeware/toga/issues/3020), [#3029](https://github.com/beeware/toga/issues/3029), [#3030](https://github.com/beeware/toga/issues/3030), [#3031](https://github.com/beeware/toga/issues/3031), [#3039](https://github.com/beeware/toga/issues/3039), [#3040](https://github.com/beeware/toga/issues/3040), [#3041](https://github.com/beeware/toga/issues/3041), [#3042](https://github.com/beeware/toga/issues/3042), [#3044](https://github.com/beeware/toga/issues/3044), [#3047](https://github.com/beeware/toga/issues/3047), [#3048](https://github.com/beeware/toga/issues/3048), [#3051](https://github.com/beeware/toga/issues/3051), [#3053](https://github.com/beeware/toga/issues/3053), [#3055](https://github.com/beeware/toga/issues/3055), [#3057](https://github.com/beeware/toga/issues/3057), [#3058](https://github.com/beeware/toga/issues/3058), [#3060](https://github.com/beeware/toga/issues/3060), [#3061](https://github.com/beeware/toga/issues/3061), [#3061](https://github.com/beeware/toga/issues/3061), [#3062](https://github.com/beeware/toga/issues/3062), [#3064](https://github.com/beeware/toga/issues/3064), [#3065](https://github.com/beeware/toga/issues/3065), [#3071](https://github.com/beeware/toga/issues/3071), [#3072](https://github.com/beeware/toga/issues/3072), [#3073](https://github.com/beeware/toga/issues/3073), [#3074](https://github.com/beeware/toga/issues/3074), [#3075](https://github.com/beeware/toga/issues/3075), [#3076](https://github.com/beeware/toga/issues/3076), [#3077](https://github.com/beeware/toga/issues/3077), [#3078](https://github.com/beeware/toga/issues/3078), [#3079](https://github.com/beeware/toga/issues/3079), [#3080](https://github.com/beeware/toga/issues/3080), [#3081](https://github.com/beeware/toga/issues/3081), [#3082](https://github.com/beeware/toga/issues/3082), [#3089](https://github.com/beeware/toga/issues/3089), [#3091](https://github.com/beeware/toga/issues/3091), [#3092](https://github.com/beeware/toga/issues/3092), [#3093](https://github.com/beeware/toga/issues/3093), [#3094](https://github.com/beeware/toga/issues/3094), [#3095](https://github.com/beeware/toga/issues/3095), [#3096](https://github.com/beeware/toga/issues/3096), [#3097](https://github.com/beeware/toga/issues/3097), [#3098](https://github.com/beeware/toga/issues/3098), [#3099](https://github.com/beeware/toga/issues/3099), [#3100](https://github.com/beeware/toga/issues/3100), [#3101](https://github.com/beeware/toga/issues/3101), [#3102](https://github.com/beeware/toga/issues/3102), [#3103](https://github.com/beeware/toga/issues/3103), [#3104](https://github.com/beeware/toga/issues/3104), [#3115](https://github.com/beeware/toga/issues/3115), [#3117](https://github.com/beeware/toga/issues/3117), [#3120](https://github.com/beeware/toga/issues/3120), [#3121](https://github.com/beeware/toga/issues/3121), [#3122](https://github.com/beeware/toga/issues/3122), [#3123](https://github.com/beeware/toga/issues/3123), [#3124](https://github.com/beeware/toga/issues/3124), [#3125](https://github.com/beeware/toga/issues/3125), [#3132](https://github.com/beeware/toga/issues/3132), [#3133](https://github.com/beeware/toga/issues/3133), [#3141](https://github.com/beeware/toga/issues/3141), [#3144](https://github.com/beeware/toga/issues/3144), [#3145](https://github.com/beeware/toga/issues/3145), [#3146](https://github.com/beeware/toga/issues/3146), [#3147](https://github.com/beeware/toga/issues/3147), [#3148](https://github.com/beeware/toga/issues/3148), [#3149](https://github.com/beeware/toga/issues/3149), [#3150](https://github.com/beeware/toga/issues/3150), [#3151](https://github.com/beeware/toga/issues/3151), [#3154](https://github.com/beeware/toga/issues/3154), [#3165](https://github.com/beeware/toga/issues/3165), [#3166](https://github.com/beeware/toga/issues/3166), [#3169](https://github.com/beeware/toga/issues/3169), [#3173](https://github.com/beeware/toga/issues/3173), [#3174](https://github.com/beeware/toga/issues/3174), [#3175](https://github.com/beeware/toga/issues/3175), [#3176](https://github.com/beeware/toga/issues/3176), [#3178](https://github.com/beeware/toga/issues/3178), [#3183](https://github.com/beeware/toga/issues/3183), [#3184](https://github.com/beeware/toga/issues/3184), [#3186](https://github.com/beeware/toga/issues/3186), [#3189](https://github.com/beeware/toga/issues/3189), [#3190](https://github.com/beeware/toga/issues/3190), [#3191](https://github.com/beeware/toga/issues/3191), [#3196](https://github.com/beeware/toga/issues/3196), [#3197](https://github.com/beeware/toga/issues/3197), [#3198](https://github.com/beeware/toga/issues/3198), [#3199](https://github.com/beeware/toga/issues/3199), [#3200](https://github.com/beeware/toga/issues/3200), [#3201](https://github.com/beeware/toga/issues/3201), [#3202](https://github.com/beeware/toga/issues/3202), [#3203](https://github.com/beeware/toga/issues/3203), [#3204](https://github.com/beeware/toga/issues/3204), [#3205](https://github.com/beeware/toga/issues/3205), [#3206](https://github.com/beeware/toga/issues/3206), [#3207](https://github.com/beeware/toga/issues/3207), [#3208](https://github.com/beeware/toga/issues/3208), [#3209](https://github.com/beeware/toga/issues/3209), [#3210](https://github.com/beeware/toga/issues/3210), [#3212](https://github.com/beeware/toga/issues/3212), [#3213](https://github.com/beeware/toga/issues/3213), [#3216](https://github.com/beeware/toga/issues/3216), [#3219](https://github.com/beeware/toga/issues/3219), [#3220](https://github.com/beeware/toga/issues/3220), [#3221](https://github.com/beeware/toga/issues/3221), [#3222](https://github.com/beeware/toga/issues/3222), [#3223](https://github.com/beeware/toga/issues/3223), [#3224](https://github.com/beeware/toga/issues/3224), [#3225](https://github.com/beeware/toga/issues/3225), [#3226](https://github.com/beeware/toga/issues/3226), [#3227](https://github.com/beeware/toga/issues/3227), [#3228](https://github.com/beeware/toga/issues/3228), [#3229](https://github.com/beeware/toga/issues/3229), [#3230](https://github.com/beeware/toga/issues/3230), [#3231](https://github.com/beeware/toga/issues/3231), [#3232](https://github.com/beeware/toga/issues/3232), [#3233](https://github.com/beeware/toga/issues/3233), [#3243](https://github.com/beeware/toga/issues/3243), [#3244](https://github.com/beeware/toga/issues/3244), [#3245](https://github.com/beeware/toga/issues/3245), [#3246](https://github.com/beeware/toga/issues/3246), [#3247](https://github.com/beeware/toga/issues/3247), [#3248](https://github.com/beeware/toga/issues/3248), [#3249](https://github.com/beeware/toga/issues/3249), [#3250](https://github.com/beeware/toga/issues/3250), [#3251](https://github.com/beeware/toga/issues/3251), [#3252](https://github.com/beeware/toga/issues/3252), [#3253](https://github.com/beeware/toga/issues/3253), [#3254](https://github.com/beeware/toga/issues/3254), [#3255](https://github.com/beeware/toga/issues/3255), [#3257](https://github.com/beeware/toga/issues/3257), [#3258](https://github.com/beeware/toga/issues/3258)

## 0.4.9 (2025-02-07)

This release contains no new features. The primary purpose of this release is to add an upper version pin to Toga's Travertino requirement, protecting against the upcoming Toga 0.5.0 release that will include backwards incompatible changes in Travertino. ([#3167](https://github.com/beeware/toga/issues/3167))

### Bugfixes

- The testbed app can now be run on *any* supported Python version. ([#2883](https://github.com/beeware/toga/issues/2883))
- App.app is now set to an initial value of `None`, before an app instance is created. This avoids a potential `AttributeError` when the test suite finishes. ([#2918](https://github.com/beeware/toga/issues/2918))

### Misc

- [#2476](https://github.com/beeware/toga/issues/2476), [#2913](https://github.com/beeware/toga/issues/2913)

## 0.4.8 (2024-10-16)

### Bugfixes

- On macOS, apps that specify both *document_types* and a *main_window* no longer display the document selection dialog on startup. ([#2860](https://github.com/beeware/toga/issues/2860))
- The integration with Android's event loop has been updated to support Python 3.13. ([#2907](https://github.com/beeware/toga/issues/2907))

### Backward Incompatible Changes

- Toga no longer supports Python 3.8. ([#2888](https://github.com/beeware/toga/issues/2888))
- Android applications should update their Gradle requirements to use version 1.12.0 of the Material library (`com.google.android.material:material:1.12.0`). ([#2890](https://github.com/beeware/toga/issues/2890))
- Android applications should update their Gradle requirements to use version 6.1.20 of the OSMDroid library (`org.osmdroid:osmdroid-android:6.1.20`). ([#2890](https://github.com/beeware/toga/issues/2890))

### Misc

- [#2868](https://github.com/beeware/toga/issues/2868), [#2869](https://github.com/beeware/toga/issues/2869), [#2870](https://github.com/beeware/toga/issues/2870), [#2876](https://github.com/beeware/toga/issues/2876), [#2877](https://github.com/beeware/toga/issues/2877), [#2884](https://github.com/beeware/toga/issues/2884), [#2885](https://github.com/beeware/toga/issues/2885), [#2886](https://github.com/beeware/toga/issues/2886), [#2887](https://github.com/beeware/toga/issues/2887), [#2893](https://github.com/beeware/toga/issues/2893), [#2897](https://github.com/beeware/toga/issues/2897), [#2898](https://github.com/beeware/toga/issues/2898), [#2899](https://github.com/beeware/toga/issues/2899), [#2900](https://github.com/beeware/toga/issues/2900), [#2901](https://github.com/beeware/toga/issues/2901), [#2902](https://github.com/beeware/toga/issues/2902), [#2903](https://github.com/beeware/toga/issues/2903), [#2904](https://github.com/beeware/toga/issues/2904), [#2905](https://github.com/beeware/toga/issues/2905), [#2906](https://github.com/beeware/toga/issues/2906), [#2912](https://github.com/beeware/toga/issues/2912)

## 0.4.7 (2024-09-18)

### Features

- The GTK backend was modified to use PyGObject's native asyncio handling, instead of GBulb. ([#2550](https://github.com/beeware/toga/issues/2550))
- The ActivityIndicator widget is now supported on iOS. ([#2829](https://github.com/beeware/toga/issues/2829))

### Bugfixes

- Windows retain their original size after being unminimized on Windows. ([#2729](https://github.com/beeware/toga/issues/2729))
- DOM storage is now enabled for WebView on Android. ([#2767](https://github.com/beeware/toga/issues/2767))
- A macOS app in full-screen mode now correctly displays the contents of windows that use a `toga.Box()` as the top-level content. ([#2796](https://github.com/beeware/toga/issues/2796))
- Asynchronous tasks are now protected from garbage collection while they are running. This could lead to asynchronous tasks terminating unexpectedly with an error under some conditions. ([#2809](https://github.com/beeware/toga/issues/2809))
- When a handler is a generator, control will now always be released to the event loop between iterations, even if no sleep interval or a sleep interval of 0 is yielded. ([#2811](https://github.com/beeware/toga/issues/2811))
- When the X button is clicked for the About dialog on GTK, it is now properly destroyed. ([#2812](https://github.com/beeware/toga/issues/2812))
- The Textual backend is now compatible with versions of Textual after v0.63.3. ([#2822](https://github.com/beeware/toga/issues/2822))
- The event loop is now guaranteed to be running when your app's `startup()` method is invoked. This wasn't previously the case on macOS and Windows. ([#2834](https://github.com/beeware/toga/issues/2834))
- iOS apps now correctly account for the size of the navigation bar when laying out app content. ([#2836](https://github.com/beeware/toga/issues/2836))
- A memory leak when using Divider or Switch widgets on iOS was resolved. ([#2849](https://github.com/beeware/toga/issues/2849))
- Apps bundled as standalone frozen binaries (e.g., POSIX builds made with PyInstaller) no longer crash on startup when trying to resolve the app icon. ([#2852](https://github.com/beeware/toga/issues/2852))

### Misc

- [#2088](https://github.com/beeware/toga/issues/2088), [#2708](https://github.com/beeware/toga/issues/2708), [#2715](https://github.com/beeware/toga/issues/2715), [#2792](https://github.com/beeware/toga/issues/2792), [#2799](https://github.com/beeware/toga/issues/2799), [#2802](https://github.com/beeware/toga/issues/2802), [#2803](https://github.com/beeware/toga/issues/2803), [#2804](https://github.com/beeware/toga/issues/2804), [#2807](https://github.com/beeware/toga/issues/2807), [#2823](https://github.com/beeware/toga/issues/2823), [#2824](https://github.com/beeware/toga/issues/2824), [#2825](https://github.com/beeware/toga/issues/2825), [#2826](https://github.com/beeware/toga/issues/2826), [#2846](https://github.com/beeware/toga/issues/2846), [#2847](https://github.com/beeware/toga/issues/2847), [#2848](https://github.com/beeware/toga/issues/2848)

## 0.4.6 (2024-08-28)

### Features

- Toga can now define apps that persist in the background without having any open windows. ([#97](https://github.com/beeware/toga/issues/97))
- Apps can now add items to the system tray. ([#97](https://github.com/beeware/toga/issues/97))
- It is now possible to use an instance of Window as the main window of an app. This allows the creation of windows that don't have a menu bar or toolbar decoration. ([#1870](https://github.com/beeware/toga/issues/1870))
- The initial position of each newly created window is now different, cascading down the screen as windows are created. ([#2023](https://github.com/beeware/toga/issues/2023))
- The API for Documents and document types has been finalized. Document handling behavior is now controlled by declaring document types as part of your `toga.App` definition. ([#2209](https://github.com/beeware/toga/issues/2209))
- Toga can now define an app whose life cycle isn't tied to a single main window. ([#2209](https://github.com/beeware/toga/issues/2209))
- The Divider widget was implemented on iOS. ([#2478](https://github.com/beeware/toga/issues/2478))
- Commands can now be retrieved by ID. System-installed commands (such as "About" and "Visit Homepage") are installed using a known ID that can be used at runtime to manipulate those commands. ([#2636](https://github.com/beeware/toga/issues/2636))
- A `MainWindow` can now have an `on_close` handler. If a request is made to close the main window, the `on_close` handler will be evaluated; app exit handling will only be processed if the close handler allows the close to continue. ([#2643](https://github.com/beeware/toga/issues/2643))
- Dialogs can now be displayed relative to an app, in addition to be being modal to a window. ([#2669](https://github.com/beeware/toga/issues/2669))
- An `on_running` event handler was added to `toga.App`. This event will be triggered when the app's main loop starts. ([#2678](https://github.com/beeware/toga/issues/2678))
- The `on_exit` handler for an app can now be defined by overriding the method on the `toga.App` subclass. ([#2678](https://github.com/beeware/toga/issues/2678))
- CommandSet now exposes a full set and dictionary interface. Commands can be added to a CommandSet using `[]` notation and a command ID; they can be removed using set-like `remove()` or `discard()` calls with a Command instance, or using dictionary-like `pop()` or `del` calls with the command ID. ([#2701](https://github.com/beeware/toga/issues/2701))
- WebView2 on Winforms now uses the v1.0.2592.51 WebView2 runtime DLLs. ([#2764](https://github.com/beeware/toga/issues/2764))

### Bugfixes

- The order of creation of system-level commands is now consistent between platforms. Menu creation is guaranteed to be deferred until the user's startup method has been invoked. ([#2619](https://github.com/beeware/toga/issues/2619))
- The type of SplitContainer's content was modified to be a list, rather than a tuple. ([#2638](https://github.com/beeware/toga/issues/2638))
- Programmatically invoking `close()` on the main window will now trigger `on_exit` handling. Previously `on_exit` handling would only be triggered if the close was initiated by a user action. ([#2643](https://github.com/beeware/toga/issues/2643))
- GTK apps no longer have extra padding between the menu bar and the window content when the app does not have a toolbar. ([#2646](https://github.com/beeware/toga/issues/2646))
- On Winforms, the window of an application that is set as the main window is no longer shown as a result of assigning the window as `App.main_window`. ([#2653](https://github.com/beeware/toga/issues/2653))
- Menu items on macOS are now able to correctly bind to the arrow and home/end/delete keys. ([#2661](https://github.com/beeware/toga/issues/2661))
- On GTK, the currently selected tab index on an `OptionContainer` can now be retrieved inside an `on_select` handler. ([#2703](https://github.com/beeware/toga/issues/2703))
- The WebView can now be loaded when using Python from the Windows Store. ([#2752](https://github.com/beeware/toga/issues/2752))
- The WebView and MapView widgets now log an error if initialization fails. ([#2779](https://github.com/beeware/toga/issues/2779))

### Backward Incompatible Changes

- The `add_background_task()` API on `toga.App` has been deprecated. Background tasks can be implemented using the new `on_running` event handler, or by using `asyncio.create_task`{.interpreted-text role="any"}. ([#2099](https://github.com/beeware/toga/issues/2099))

- The API for Documents and Document-based apps has been significantly modified. Unfortunately, these changes are not backwards compatible; any existing Document-based app will require modification.  The `DocumentApp` base class is no longer required. Apps can subclass `App` directly, passing the document types as a `list` of `Document` classes, rather than a mapping of extension to document type.  The API for `Document` subclasses has also changed:
    - A path is no longer provided as an argument to the Document constructor;
    - The `document_type` is now specified as a class property called `description`; and
    - Extensions are now defined as a class property of the `Document`; and
    - The `can_close()` handler is no longer honored. Documents now track if they are modified, and have a default `on_close` handler that uses the modification status of a document to control whether a document can close. Invoking `touch()` on document will mark a document as modified. This modification flag is cleared by saving the document. ([#2209](https://github.com/beeware/toga/issues/2209))

- It is no longer possible to create a toolbar on a `Window` instance. Toolbars can only be added to `MainWindow` (or subclass). ([#2646](https://github.com/beeware/toga/issues/2646))

- The default title of a `toga.Window` is now the name of the app, rather than `"Toga"`. ([#2646](https://github.com/beeware/toga/issues/2646))

- The APIs on `Window` for displaying dialogs (`info_dialog()`, `question_dialog()`, etc) have been deprecated. They can be replaced with creating an instance of a `Dialog` class (e.g., `InfoDialog`), and passing that instance to `window.dialog()`. ([#2669](https://github.com/beeware/toga/issues/2669))

### Documentation

- Building Toga's documentation now requires the use of Python 3.12. ([#2745](https://github.com/beeware/toga/issues/2745))

### Misc

- [#2382](https://github.com/beeware/toga/issues/2382), [#2635](https://github.com/beeware/toga/issues/2635), [#2640](https://github.com/beeware/toga/issues/2640), [#2647](https://github.com/beeware/toga/issues/2647), [#2648](https://github.com/beeware/toga/issues/2648), [#2654](https://github.com/beeware/toga/issues/2654), [#2657](https://github.com/beeware/toga/issues/2657), [#2660](https://github.com/beeware/toga/issues/2660), [#2665](https://github.com/beeware/toga/issues/2665), [#2668](https://github.com/beeware/toga/issues/2668), [#2675](https://github.com/beeware/toga/issues/2675), [#2676](https://github.com/beeware/toga/issues/2676), [#2677](https://github.com/beeware/toga/issues/2677), [#2682](https://github.com/beeware/toga/issues/2682), [#2683](https://github.com/beeware/toga/issues/2683), [#2684](https://github.com/beeware/toga/issues/2684), [#2689](https://github.com/beeware/toga/issues/2689), [#2693](https://github.com/beeware/toga/issues/2693), [#2694](https://github.com/beeware/toga/issues/2694), [#2695](https://github.com/beeware/toga/issues/2695), [#2696](https://github.com/beeware/toga/issues/2696), [#2697](https://github.com/beeware/toga/issues/2697), [#2698](https://github.com/beeware/toga/issues/2698), [#2699](https://github.com/beeware/toga/issues/2699), [#2709](https://github.com/beeware/toga/issues/2709), [#2710](https://github.com/beeware/toga/issues/2710), [#2711](https://github.com/beeware/toga/issues/2711), [#2712](https://github.com/beeware/toga/issues/2712), [#2722](https://github.com/beeware/toga/issues/2722), [#2723](https://github.com/beeware/toga/issues/2723), [#2724](https://github.com/beeware/toga/issues/2724), [#2726](https://github.com/beeware/toga/issues/2726), [#2727](https://github.com/beeware/toga/issues/2727), [#2728](https://github.com/beeware/toga/issues/2728), [#2733](https://github.com/beeware/toga/issues/2733), [#2734](https://github.com/beeware/toga/issues/2734), [#2735](https://github.com/beeware/toga/issues/2735), [#2736](https://github.com/beeware/toga/issues/2736), [#2739](https://github.com/beeware/toga/issues/2739), [#2740](https://github.com/beeware/toga/issues/2740), [#2742](https://github.com/beeware/toga/issues/2742), [#2743](https://github.com/beeware/toga/issues/2743), [#2755](https://github.com/beeware/toga/issues/2755), [#2756](https://github.com/beeware/toga/issues/2756), [#2757](https://github.com/beeware/toga/issues/2757), [#2758](https://github.com/beeware/toga/issues/2758), [#2760](https://github.com/beeware/toga/issues/2760), [#2771](https://github.com/beeware/toga/issues/2771), [#2775](https://github.com/beeware/toga/issues/2775), [#2776](https://github.com/beeware/toga/issues/2776), [#2777](https://github.com/beeware/toga/issues/2777), [#2783](https://github.com/beeware/toga/issues/2783), [#2788](https://github.com/beeware/toga/issues/2788), [#2789](https://github.com/beeware/toga/issues/2789), [#2790](https://github.com/beeware/toga/issues/2790)

## 0.4.5 (2024-06-11)

### Features

- The typing for Toga's API surface was updated to be more precise. ([#2252](https://github.com/beeware/toga/issues/2252))
- APIs were added for replacing a widget in an existing layout, and for obtaining the index of a widget in a list of children. ([#2301](https://github.com/beeware/toga/issues/2301))
- The content of a window can now be set when the window is constructed. ([#2307](https://github.com/beeware/toga/issues/2307))
- Size and position properties now return values as a `Size` and `Position` `namedtuple`, respectively. `namedtuple` objects support addition and subtraction operations. Basic tuples can still be used to *set* these properties. ([#2388](https://github.com/beeware/toga/issues/2388))
- Android deployments no longer require the SwipeRefreshLayout component unless the app uses the Toga DetailedList widget. ([#2454](https://github.com/beeware/toga/issues/2454))

### Bugfixes

- Invocation order of TextInput on_change and validation is now correct. ([#2325](https://github.com/beeware/toga/issues/2325))
- Dialog windows are now properly modal when using the GTK backend. ([#2446](https://github.com/beeware/toga/issues/2446))
- The Button testbed tests can accommodate minor rendering differences on Fedora 40. ([#2583](https://github.com/beeware/toga/issues/2583))
- On macOS, apps will now raise a warning if camera permissions have been requested, but those permissions have not been declared as part of the application metadata. ([#2589](https://github.com/beeware/toga/issues/2589))

### Documentation

- The instructions for adding a change note to a pull request have been clarified. ([#2565](https://github.com/beeware/toga/issues/2565))
- The minimum supported Linux release requirements were updated to Ubuntu 20.04 or Fedora 32. ([#2566](https://github.com/beeware/toga/issues/2566))
- The first-time contributor README link has been updated. ([#2588](https://github.com/beeware/toga/issues/2588))
- Typos in the usage examples of `toga.MapPin` were corrected. ([#2617](https://github.com/beeware/toga/issues/2617))

### Misc

- [#2567](https://github.com/beeware/toga/issues/2567), [#2568](https://github.com/beeware/toga/issues/2568), [#2569](https://github.com/beeware/toga/issues/2569), [#2570](https://github.com/beeware/toga/issues/2570), [#2571](https://github.com/beeware/toga/issues/2571), [#2576](https://github.com/beeware/toga/issues/2576), [#2577](https://github.com/beeware/toga/issues/2577), [#2578](https://github.com/beeware/toga/issues/2578), [#2579](https://github.com/beeware/toga/issues/2579), [#2580](https://github.com/beeware/toga/issues/2580), [#2593](https://github.com/beeware/toga/issues/2593), [#2600](https://github.com/beeware/toga/issues/2600), [#2601](https://github.com/beeware/toga/issues/2601), [#2602](https://github.com/beeware/toga/issues/2602), [#2604](https://github.com/beeware/toga/issues/2604), [#2605](https://github.com/beeware/toga/issues/2605), [#2606](https://github.com/beeware/toga/issues/2606), [#2614](https://github.com/beeware/toga/issues/2614), [#2621](https://github.com/beeware/toga/issues/2621), [#2625](https://github.com/beeware/toga/issues/2625), [#2626](https://github.com/beeware/toga/issues/2626), [#2627](https://github.com/beeware/toga/issues/2627), [#2629](https://github.com/beeware/toga/issues/2629), [#2631](https://github.com/beeware/toga/issues/2631), [#2632](https://github.com/beeware/toga/issues/2632)

## 0.4.4 (2024-05-08)

### Bugfixes

- The mechanism for loading application icons on macOS was corrected to account for how Xcode populates `Info.plist` metadata. ([#2558](https://github.com/beeware/toga/issues/2558))

### Misc

- [#2555](https://github.com/beeware/toga/issues/2555), [#2557](https://github.com/beeware/toga/issues/2557), [#2560](https://github.com/beeware/toga/issues/2560)

## 0.4.3 (2024-05-06)

### Features

- A MapView widget was added. ([#727](https://github.com/beeware/toga/issues/727))
- Toga apps can now access details about the screens attached to the computer. Window position APIs have been extended to allow for placement on a specific screen, and positioning relative to a specific screen. ([#1930](https://github.com/beeware/toga/issues/1930))
- Key definitions were added for number pad keys on GTK. ([#2232](https://github.com/beeware/toga/issues/2232))
- Toga can now be extended, via plugins, to create Toga Images from external image classes (and vice-versa). ([#2387](https://github.com/beeware/toga/issues/2387))
- Non-implemented features now raise a formal warning, rather than logging to the console. ([#2398](https://github.com/beeware/toga/issues/2398))
- Support for Python 3.13 was added. ([#2404](https://github.com/beeware/toga/issues/2404))
- Toga's release processes now include automated testing on ARM64. ([#2404](https://github.com/beeware/toga/issues/2404))
- An action for a Toga command can now be easily modified after initial construction. ([#2433](https://github.com/beeware/toga/issues/2433))
- A geolocation service was added for Android, iOS and macOS. ([#2462](https://github.com/beeware/toga/issues/2462))
- When a Toga app is packaged as a binary, and no icon is explicitly configured, Toga will now use the binary's icon as the app icon. This means it is no longer necessary to include the app icon as data in a `resources` folder if you are packaging your app for distribution. ([#2527](https://github.com/beeware/toga/issues/2527))

### Bugfixes

- Compatibility with macOS 14 (Sonoma) was added. ([#2188](https://github.com/beeware/toga/issues/2188), [#2383](https://github.com/beeware/toga/issues/2383))
- Key handling for Insert, Delete, NumLock, ScrollLock, and some other esoteric keys was added for GTK and Winforms. Some uses of bare Shift on GTK were also improved. ([#2220](https://github.com/beeware/toga/issues/2220))
- A crash observed on iOS devices when taking photographs has been resolved. ([#2381](https://github.com/beeware/toga/issues/2381))
- Key shortcuts for punctuation and special keys (like Page Up and Escape) were added for GTK and Winforms. ([#2414](https://github.com/beeware/toga/issues/2414))
- The placement of menu items relative to sub-menus was corrected on GTK. ([#2418](https://github.com/beeware/toga/issues/2418))
- Tree data nodes can now be modified prior to tree expansion. ([#2439](https://github.com/beeware/toga/issues/2439))
- Some memory leaks associated with macOS Icon and Image storage were resolved. ([#2472](https://github.com/beeware/toga/issues/2472))
- The stack trace dialog no longer raises an `asyncio.TimeoutError` when displayed. ([#2474](https://github.com/beeware/toga/issues/2474))
- The integration of the `asyncio` event loop was simplified on Android. As a result, `asyncio.loop.run_in_executor()` now works as expected. ([#2479](https://github.com/beeware/toga/issues/2479))
- Some memory leaks associated with the macOS Table, Tree and DetailedList widgets were resolved. ([#2482](https://github.com/beeware/toga/issues/2482))
- Widget IDs can now be reused after the associated widget's window is closed. ([#2514](https://github.com/beeware/toga/issues/2514))
- [WebView][toga.WebView] is now compatible with Linux GTK environments only providing WebKit2 version 4.1 without version 4.0. ([#2527](https://github.com/beeware/toga/issues/2527))

### Backward Incompatible Changes

- The macOS implementations of `Window.as_image()` and `Canvas.as_image()` APIs now return images in native device resolution, not CSS pixel resolution. This will result in images that are double the previous size on Retina displays. ([#1930](https://github.com/beeware/toga/issues/1930))

### Documentation

- The camera permission requirements on macOS apps have been clarified. ([#2381](https://github.com/beeware/toga/issues/2381))
- Documentation for the class property `toga.App.app` was added. ([#2413](https://github.com/beeware/toga/issues/2413))
- The documentation landing page and some documentation sections were reorganized. ([#2463](https://github.com/beeware/toga/issues/2463))
- The README badges were updated to display correctly on GitHub. ([#2491](https://github.com/beeware/toga/issues/2491))
- The links to Read the Docs were updated to better arbitrate between linking to the stable version or the latest version. ([#2510](https://github.com/beeware/toga/issues/2510))
- An explicit system requirements section was added to the documentation for widgets that require the installation of additional system components. ([#2544](https://github.com/beeware/toga/issues/2544))
- The system requirements were updated to be more explicit and now include details for OpenSUSE Tumbleweed. ([#2549](https://github.com/beeware/toga/issues/2549))

### Misc

- [#2153](https://github.com/beeware/toga/issues/2153), [#2372](https://github.com/beeware/toga/issues/2372), [#2389](https://github.com/beeware/toga/issues/2389), [#2390](https://github.com/beeware/toga/issues/2390), [#2391](https://github.com/beeware/toga/issues/2391), [#2392](https://github.com/beeware/toga/issues/2392), [#2393](https://github.com/beeware/toga/issues/2393), [#2394](https://github.com/beeware/toga/issues/2394), [#2396](https://github.com/beeware/toga/issues/2396), [#2397](https://github.com/beeware/toga/issues/2397), [#2400](https://github.com/beeware/toga/issues/2400), [#2403](https://github.com/beeware/toga/issues/2403), [#2405](https://github.com/beeware/toga/issues/2405), [#2406](https://github.com/beeware/toga/issues/2406), [#2407](https://github.com/beeware/toga/issues/2407), [#2408](https://github.com/beeware/toga/issues/2408), [#2409](https://github.com/beeware/toga/issues/2409), [#2422](https://github.com/beeware/toga/issues/2422), [#2423](https://github.com/beeware/toga/issues/2423), [#2427](https://github.com/beeware/toga/issues/2427), [#2440](https://github.com/beeware/toga/issues/2440), [#2442](https://github.com/beeware/toga/issues/2442), [#2445](https://github.com/beeware/toga/issues/2445), [#2448](https://github.com/beeware/toga/issues/2448), [#2449](https://github.com/beeware/toga/issues/2449), [#2450](https://github.com/beeware/toga/issues/2450), [#2457](https://github.com/beeware/toga/issues/2457), [#2458](https://github.com/beeware/toga/issues/2458), [#2459](https://github.com/beeware/toga/issues/2459), [#2460](https://github.com/beeware/toga/issues/2460), [#2464](https://github.com/beeware/toga/issues/2464), [#2465](https://github.com/beeware/toga/issues/2465), [#2466](https://github.com/beeware/toga/issues/2466), [#2467](https://github.com/beeware/toga/issues/2467), [#2470](https://github.com/beeware/toga/issues/2470), [#2471](https://github.com/beeware/toga/issues/2471), [#2476](https://github.com/beeware/toga/issues/2476), [#2487](https://github.com/beeware/toga/issues/2487), [#2488](https://github.com/beeware/toga/issues/2488), [#2498](https://github.com/beeware/toga/issues/2498), [#2501](https://github.com/beeware/toga/issues/2501), [#2502](https://github.com/beeware/toga/issues/2502), [#2503](https://github.com/beeware/toga/issues/2503), [#2504](https://github.com/beeware/toga/issues/2504), [#2509](https://github.com/beeware/toga/issues/2509), [#2518](https://github.com/beeware/toga/issues/2518), [#2519](https://github.com/beeware/toga/issues/2519), [#2520](https://github.com/beeware/toga/issues/2520), [#2521](https://github.com/beeware/toga/issues/2521), [#2522](https://github.com/beeware/toga/issues/2522), [#2523](https://github.com/beeware/toga/issues/2523), [#2532](https://github.com/beeware/toga/issues/2532), [#2533](https://github.com/beeware/toga/issues/2533), [#2534](https://github.com/beeware/toga/issues/2534), [#2535](https://github.com/beeware/toga/issues/2535), [#2536](https://github.com/beeware/toga/issues/2536), [#2537](https://github.com/beeware/toga/issues/2537), [#2538](https://github.com/beeware/toga/issues/2538), [#2539](https://github.com/beeware/toga/issues/2539), [#2540](https://github.com/beeware/toga/issues/2540), [#2541](https://github.com/beeware/toga/issues/2541), [#2542](https://github.com/beeware/toga/issues/2542), [#2546](https://github.com/beeware/toga/issues/2546), [#2552](https://github.com/beeware/toga/issues/2552)

## 0.4.2 (2024-02-06)

### Features

- Buttons can now be created with an icon, instead of a text label. ([#774](https://github.com/beeware/toga/issues/774))
- Widgets and Windows can now be sorted. The ID of the widget is used for the sorting order. ([#2190](https://github.com/beeware/toga/issues/2190))
- The main window generated by the default `startup()` method of an app now has an ID of `main`. ([#2190](https://github.com/beeware/toga/issues/2190))
- A cross-platform API for camera access was added. ([#2266](https://github.com/beeware/toga/issues/2266), [#2353](https://github.com/beeware/toga/issues/2353))
- An OptionContainer widget was added for Android. ([#2346](https://github.com/beeware/toga/issues/2346))

### Bugfixes

- New widgets with an ID matching an ID that was previously used no longer cause an error. ([#2190](https://github.com/beeware/toga/issues/2190))
- `App.current_window` on GTK now returns `None` when all windows are hidden. ([#2211](https://github.com/beeware/toga/issues/2211))
- Selection widgets on macOS can now include duplicated titles. ([#2319](https://github.com/beeware/toga/issues/2319))
- The padding around DetailedList on Android has been reduced. ([#2338](https://github.com/beeware/toga/issues/2338))
- The error returned when an Image is created with no source has been clarified. ([#2347](https://github.com/beeware/toga/issues/2347))
- On macOS, `toga.Image` objects can now be created from raw data that didn't originate from a file. ([#2355](https://github.com/beeware/toga/issues/2355))
- Winforms no longer generates a system beep when pressing Enter in a TextInput. ([#2374](https://github.com/beeware/toga/issues/2374))

### Backward Incompatible Changes

- Widgets must now be added to a window to be available in the widget registry for lookup by ID. ([#2190](https://github.com/beeware/toga/issues/2190))
- If the label for a Selection contains newlines, only the text up to the first newline will be displayed. ([#2319](https://github.com/beeware/toga/issues/2319))
- The internal Android method `intent_result` has been deprecated. This was an internal API, and not formally documented, but it was the easiest mechanism for invoking Intents on the Android backend. It has been replaced by the synchronous `start_activity` method that allows you to register a callback when the intent completes. ([#2353](https://github.com/beeware/toga/issues/2353))

### Documentation

- Initial documentation of backend-specific features has been added. ([#1798](https://github.com/beeware/toga/issues/1798))
- The difference between Icon and Image was clarified, and a note about the lack of an `on_press` handler on ImageView was added. ([#2348](https://github.com/beeware/toga/issues/2348))

### Misc

- [#2298](https://github.com/beeware/toga/issues/2298), [#2299](https://github.com/beeware/toga/issues/2299), [#2302](https://github.com/beeware/toga/issues/2302), [#2312](https://github.com/beeware/toga/issues/2312), [#2313](https://github.com/beeware/toga/issues/2313), [#2318](https://github.com/beeware/toga/issues/2318), [#2331](https://github.com/beeware/toga/issues/2331), [#2332](https://github.com/beeware/toga/issues/2332), [#2333](https://github.com/beeware/toga/issues/2333), [#2336](https://github.com/beeware/toga/issues/2336), [#2337](https://github.com/beeware/toga/issues/2337), [#2339](https://github.com/beeware/toga/issues/2339), [#2340](https://github.com/beeware/toga/issues/2340), [#2357](https://github.com/beeware/toga/issues/2357), [#2358](https://github.com/beeware/toga/issues/2358), [#2359](https://github.com/beeware/toga/issues/2359), [#2363](https://github.com/beeware/toga/issues/2363), [#2367](https://github.com/beeware/toga/issues/2367), [#2368](https://github.com/beeware/toga/issues/2368), [#2369](https://github.com/beeware/toga/issues/2369), [#2370](https://github.com/beeware/toga/issues/2370), [#2371](https://github.com/beeware/toga/issues/2371), [#2375](https://github.com/beeware/toga/issues/2375), [#2376](https://github.com/beeware/toga/issues/2376)

## 0.4.1 (2023-12-21)

### Features

- Toga images can now be created from (and converted to) PIL images. ([#2142](https://github.com/beeware/toga/issues/2142))
- A wider range of command shortcut keys are now supported on WinForms. ([#2198](https://github.com/beeware/toga/issues/2198))
- Most widgets with flexible sizes now default to a minimum size of 100 CSS pixels. An explicit size will still override this value. ([#2200](https://github.com/beeware/toga/issues/2200))
- OptionContainer content can now be constructed using `toga.OptionItem` objects. ([#2259](https://github.com/beeware/toga/issues/2259))
- An OptionContainer widget was added for iOS. ([#2259](https://github.com/beeware/toga/issues/2259))
- Apps can now specify platform-specific icon resources by appending the platform name (e.g., `-macOS` or `-windows`) to the icon filename. ([#2260](https://github.com/beeware/toga/issues/2260))
- Images can now be created from the native platform representation of an image, without needing to be transformed to bytes. ([#2263](https://github.com/beeware/toga/issues/2263))

### Bugfixes

- TableViews on macOS will no longer crash if a drag operation is initiated from inside the table. ([#1156](https://github.com/beeware/toga/issues/1156))
- Separators before and after command sub-groups are now included in menus. ([#2193](https://github.com/beeware/toga/issues/2193))
- The web backend no longer generates a duplicate title bar. ([#2194](https://github.com/beeware/toga/issues/2194))
- The web backend is now able to display the About dialog on first page load. ([#2195](https://github.com/beeware/toga/issues/2195))
- The testbed is now able to run on macOS when the user running the tests has the macOS display setting "Prefer tabs when opening documents" set to "Always". ([#2208](https://github.com/beeware/toga/issues/2208))
- Compliance with Apple's HIG regarding the naming and shortcuts for the Close and Close All menu items was improved. ([#2214](https://github.com/beeware/toga/issues/2214))
- Font handling on older versions of iOS has been corrected. ([#2265](https://github.com/beeware/toga/issues/2265))
- ImageViews with `flex=1` will now shrink to fit if the image is larger than the available space. ([#2275](https://github.com/beeware/toga/issues/2275))

### Backward Incompatible Changes

- The `toga.Image` constructor now takes a single argument (`src`); the `path` and `data` arguments are deprecated. ([#2142](https://github.com/beeware/toga/issues/2142))
- The use of Caps Lock as a keyboard modifier for commands was removed. ([#2198](https://github.com/beeware/toga/issues/2198))
- Support for macOS release prior to Big Sur (11) has been dropped. ([#2228](https://github.com/beeware/toga/issues/2228))
- When inserting or appending a tab to an OptionContainer, the `enabled` argument must now be provided as a keyword argument. The name of the first argument has been also been renamed (from `text` to `text_or_item`); it should generally be passed as a positional, rather than keyword argument. ([#2259](https://github.com/beeware/toga/issues/2259))
- The use of synchronous `on_result` callbacks on dialogs and `Webview.evaluate_javascript()` calls has been deprecated. These methods should be used in their asynchronous form. ([#2264](https://github.com/beeware/toga/issues/2264))

### Documentation

- Documentation for `toga.Key` was added. ([#2199](https://github.com/beeware/toga/issues/2199))
- Some limitations on App presentation imposed by Wayland have been documented. ([#2255](https://github.com/beeware/toga/issues/2255))

### Misc

- [#2201](https://github.com/beeware/toga/issues/2201), [#2204](https://github.com/beeware/toga/issues/2204), [#2215](https://github.com/beeware/toga/issues/2215), [#2216](https://github.com/beeware/toga/issues/2216), [#2219](https://github.com/beeware/toga/issues/2219), [#2222](https://github.com/beeware/toga/issues/2222), [#2224](https://github.com/beeware/toga/issues/2224), [#2226](https://github.com/beeware/toga/issues/2226), [#2230](https://github.com/beeware/toga/issues/2230), [#2235](https://github.com/beeware/toga/issues/2235), [#2240](https://github.com/beeware/toga/issues/2240), [#2246](https://github.com/beeware/toga/issues/2246), [#2249](https://github.com/beeware/toga/issues/2249), [#2256](https://github.com/beeware/toga/issues/2256), [#2257](https://github.com/beeware/toga/issues/2257), [#2261](https://github.com/beeware/toga/issues/2261), [#2264](https://github.com/beeware/toga/issues/2264), [#2267](https://github.com/beeware/toga/issues/2267), [#2269](https://github.com/beeware/toga/issues/2269), [#2270](https://github.com/beeware/toga/issues/2270), [#2271](https://github.com/beeware/toga/issues/2271), [#2272](https://github.com/beeware/toga/issues/2272), [#2283](https://github.com/beeware/toga/issues/2283), [#2284](https://github.com/beeware/toga/issues/2284), [#2287](https://github.com/beeware/toga/issues/2287), [#2294](https://github.com/beeware/toga/issues/2294)

## 0.4.0 (2023-11-03)

### Features

- The Toga API has been fully audited. All APIs now have 100% test coverage, complete API documentation (including type annotations), and are internally consistent. ( [#1903](https://github.com/beeware/toga/issues/1903), [#1938](https://github.com/beeware/toga/issues/1938), [#1944](https://github.com/beeware/toga/issues/1944), [#1946](https://github.com/beeware/toga/issues/1946), [#1949](https://github.com/beeware/toga/issues/1949), [#1951](https://github.com/beeware/toga/issues/1951), [#1955](https://github.com/beeware/toga/issues/1955), [#1956](https://github.com/beeware/toga/issues/1956), [#1964](https://github.com/beeware/toga/issues/1964), [#1969](https://github.com/beeware/toga/issues/1969), [#1984](https://github.com/beeware/toga/issues/1984), [#1996](https://github.com/beeware/toga/issues/1996), [#2011](https://github.com/beeware/toga/issues/2011), [#2017](https://github.com/beeware/toga/issues/2017), [#2025](https://github.com/beeware/toga/issues/2025), [#2029](https://github.com/beeware/toga/issues/2029), [#2044](https://github.com/beeware/toga/issues/2044), [#2058](https://github.com/beeware/toga/issues/2058), [#2075](https://github.com/beeware/toga/issues/2075))
- Headings are no longer mandatory for Tree widgets. If headings are not provided, the widget will not display its header bar. ([#1767](https://github.com/beeware/toga/issues/1767))
- Support for custom font loading was added to the GTK, Cocoa and iOS backends. ([#1837](https://github.com/beeware/toga/issues/1837))
- The testbed app has better diagnostic output when running in test mode. ([#1847](https://github.com/beeware/toga/issues/1847))
- A Textual backend was added to support terminal applications. ([#1867](https://github.com/beeware/toga/issues/1867))
- Support for determining the currently active window was added to Winforms. ([#1872](https://github.com/beeware/toga/issues/1872))
- Programmatically scrolling to top and bottom in MultilineTextInput is now possible on iOS. ([#1876](https://github.com/beeware/toga/issues/1876))
- A handler has been added for users confirming the contents of a TextInput by pressing Enter/Return. ([#1880](https://github.com/beeware/toga/issues/1880))
- An API for giving a window focus was added. ([#1887](https://github.com/beeware/toga/issues/1887))
- Widgets now have a `.clear()` method to remove all child widgets. ([#1893](https://github.com/beeware/toga/issues/1893))
- Winforms now supports hiding and re-showing the app cursor. ([#1894](https://github.com/beeware/toga/issues/1894))
- ProgressBar and Switch widgets were added to the Web backend. ([#1901](https://github.com/beeware/toga/issues/1901))
- Missing value handling was added to the Tree widget. ([#1913](https://github.com/beeware/toga/issues/1913))
- App paths now include a `config` path for storing configuration files. ([#1964](https://github.com/beeware/toga/issues/1964))
- A more informative error message is returned when a platform backend doesn't support a widget. ([#1992](https://github.com/beeware/toga/issues/1992))
- The example apps were updated to support being run with `briefcase run` on all platforms. ([#1995](https://github.com/beeware/toga/issues/1995))
- Headings are no longer mandatory Table widgets. ([#2011](https://github.com/beeware/toga/issues/2011))
- Columns can now be added and removed from a Tree. ([#2017](https://github.com/beeware/toga/issues/2017))
- The default system notification sound can be played via `App.beep()`. ([#2018](https://github.com/beeware/toga/issues/2018))
- DetailedList can now respond to "primary" and "secondary" user actions. These may be implemented as left and right swipe respectively, or using any other platform-appropriate mechanism. ([#2025](https://github.com/beeware/toga/issues/2025))
- A DetailedList can now provide a value to use when a row doesn't provide the required data. ([#2025](https://github.com/beeware/toga/issues/2025))
- The accessors used to populate a DetailedList can now be customized. ([#2025](https://github.com/beeware/toga/issues/2025))
- Transformations can now be applied to *any* canvas context, not just the root context. ([#2029](https://github.com/beeware/toga/issues/2029))
- Canvas now provides more `list`-like methods for manipulating drawing objects in a context. ([#2029](https://github.com/beeware/toga/issues/2029))
- On Windows, the default font now follows the system theme. On most devices, this means it has changed from Microsoft Sans Serif 8pt to Segoe UI 9pt. ([#2029](https://github.com/beeware/toga/issues/2029))
- Font sizes are now consistently interpreted as CSS points. On Android, iOS and macOS, this means any numeric font sizes will appear 33% larger than before. The default font size on these platforms is unchanged. ([#2029](https://github.com/beeware/toga/issues/2029))
- MultilineTextInputs no longer show spelling suggestions when in read-only mode. ([#2136](https://github.com/beeware/toga/issues/2136))
- Applications now verify that a main window has been created as part of the `startup()` method. ([#2047](https://github.com/beeware/toga/issues/2047))
- An implementation of ActivityIndicator was added to the Web backend. ([#2050](https://github.com/beeware/toga/issues/2050))
- An implementation of Divider was added to the Web backend. ([#2051](https://github.com/beeware/toga/issues/2051))
- The ability to capture the contents of a window as an image has been added. ([#2063](https://github.com/beeware/toga/issues/2063))
- A PasswordInput widget was added to the Web backend. ([#2089](https://github.com/beeware/toga/issues/2089))
- The WebKit inspector is automatically enabled on all macOS WebViews, provided you're using macOS 13.3 (Ventura) or iOS 16.4, or later. ([#2109](https://github.com/beeware/toga/issues/2109))
- Text input widgets on macOS now support undo and redo. ([#2151](https://github.com/beeware/toga/issues/2151))
- The Divider widget was implemented on Android. ([#2181](https://github.com/beeware/toga/issues/2181))

### Bugfixes

- The WinForms event loop was decoupled from the main form, allowing background tasks to run without a main window being present. ([#750](https://github.com/beeware/toga/issues/750))
- Widgets are now removed from windows when the window is closed, preventing a memory leak on window closure. ([#1215](https://github.com/beeware/toga/issues/1215))
- Android and iOS apps no longer crash if you invoke `App.hide_cursor()` or `App.show_cursor()`. ([#1235](https://github.com/beeware/toga/issues/1235))
- A Selection widget with no items now consistently returns a selected value of `None` on all platforms. ([#1723](https://github.com/beeware/toga/issues/1723))
- macOS widget methods that return strings are now guaranteed to return strings, rather than native Objective C string objects. ([#1779](https://github.com/beeware/toga/issues/1779))
- WebViews on Windows no longer have a black background when they are resized. ([#1855](https://github.com/beeware/toga/issues/1855))
- The interpretation of `MultilineTextInput.readonly` was corrected iOS ([#1866](https://github.com/beeware/toga/issues/1866))
- A window without an `on_close` handler can now be closed using the window frame close button. ([#1872](https://github.com/beeware/toga/issues/1872))
- Android apps running on devices older than API level 29 (Android 10) no longer crash. ([#1878](https://github.com/beeware/toga/issues/1878))
- Missing value handling on Tables was fixed on Android and Linux. ([#1879](https://github.com/beeware/toga/issues/1879))
- The GTK backend is now able to correctly identify the currently active window. ([#1892](https://github.com/beeware/toga/issues/1892))
- Error handling associated with the creation of Intents on Android has been improved. ([#1909](https://github.com/beeware/toga/issues/1909))
- The DetailedList widget on GTK now provides an accurate size hint during layout. ([#1920](https://github.com/beeware/toga/issues/1920))
- Apps on Linux no longer segfault if an X Windows display cannot be identified. ([#1921](https://github.com/beeware/toga/issues/1921))
- The `on_result` handler is now used by Cocoa file dialogs. ([#1947](https://github.com/beeware/toga/issues/1947))
- Pack layout now honors an explicit width/height setting of 0. ([#1958](https://github.com/beeware/toga/issues/1958))
- The minimum window size is now correctly recomputed and enforced if window content changes. ([#2020](https://github.com/beeware/toga/issues/2020))
- The title of windows can now be modified on Winforms. ([#2094](https://github.com/beeware/toga/issues/2094))
- An error on Winforms when a window has no content has been resolved. ([#2095](https://github.com/beeware/toga/issues/2095))
- iOS container views are now set to automatically resize with their parent view ([#2161](https://github.com/beeware/toga/issues/2161))

### Backward Incompatible Changes

- The `weight`, `style` and `variant` arguments for `Font` and `Font.register` are now keyword-only. ([#1903](https://github.com/beeware/toga/issues/1903))
- The `clear()` method for resetting the value of a MultilineTextInput, TextInput and PasswordInput has been removed. This method was an ambiguous override of the `clear()` method on Widget that removed all child nodes. To remove all content from a text input widget, use `widget.value = ""`. ([#1938](https://github.com/beeware/toga/issues/1938))
- The ability to perform multiple substring matches in a `Contains` validator has been removed. ([#1944](https://github.com/beeware/toga/issues/1944))
- The `TextInput.validate` method has been removed. Validation now happens automatically whenever the `value` or `validators` properties are changed. ([#1944](https://github.com/beeware/toga/issues/1944))
- The argument names used to construct validators have changed. Error message arguments now all end with `_message`; `compare_count` has been renamed `count`; and `min_value` and `max_value` have been renamed `min_length` and `max_length`, respectively. ([#1944](https://github.com/beeware/toga/issues/1944))
- The `get_dom()` method on WebView has been removed. This method wasn't implemented on most platforms, and wasn't working on any of the platforms where it *was* implemented, as modern web view implementations don't provide a synchronous API for accessing web content in this way. ([#1949](https://github.com/beeware/toga/issues/1949))
- The `evaluate_javascript()` method on WebView has been modified to work in both synchronous and asynchronous contexts. In a synchronous context you can invoke the method and use a functional `on_result` callback to be notified when evaluation is complete. In an asynchronous context, you can await the result. ([#1949](https://github.com/beeware/toga/issues/1949))
- The `on_key_down` handler has been removed from WebView. If you need to catch user input, either use a handler in the embedded JavaScript, or create a `Command` with a key shortcut. ([#1949](https://github.com/beeware/toga/issues/1949))
- The `invoke_javascript()` method has been removed. All usage of `invoke_javascript()` can be replaced with `evaluate_javascript()`. ([#1949](https://github.com/beeware/toga/issues/1949))
- The usage of local `file://` URLs has been explicitly prohibited. `file://` URLs have not been reliable for some time; their usage is now explicitly prohibited. ([#1949](https://github.com/beeware/toga/issues/1949))
- `DatePicker` has been renamed `DateInput`. ([#1951](https://github.com/beeware/toga/issues/1951))
- `TimePicker` has been renamed `TimeInput`. ([#1951](https://github.com/beeware/toga/issues/1951))
- The `on_select` handler on the Selection widget has been renamed `on_change` for consistency with other widgets. ([#1955](https://github.com/beeware/toga/issues/1955))
- The `_notify()` method on data sources has been renamed `notify()`, reflecting its status as a public API. ([#1955](https://github.com/beeware/toga/issues/1955))
- The `prepend()` method was removed from the `ListSource` and `TreeSource` APIs. Calls to `prepend(...)` can be replaced with `insert(0, ...)`. ([#1955](https://github.com/beeware/toga/issues/1955))
- The `insert()` and `append()` APIs on `ListSource` and `TreeSource` have been modified to provide an interface that is closer to that `list` API. These methods previously accepted a variable list of positional and keyword arguments; these arguments should be combined into a single tuple or dictionary. This matches the API provided by `__setitem__()`. ([#1955](https://github.com/beeware/toga/issues/1955))
- Images and ImageViews no longer support loading images from URLs. If you need to display an image from a URL, use a background task to obtain the image data asynchronously, then create the Image and/or set the ImageView `image` property on the completion of the asynchronous load. ([#1956](https://github.com/beeware/toga/issues/1956))
- A row box contained inside a row box will now expand to the full height of its parent, rather than collapsing to the maximum height of the inner box's child content. ([#1958](https://github.com/beeware/toga/issues/1958))
- A column box contained inside a column box will now expand to the full width of its parent, rather than collapsing to the maximum width of the inner box's child content. ([#1958](https://github.com/beeware/toga/issues/1958))
- On Android, the user data folder is now a `data` sub-directory of the location returned by `context.getFilesDir()`, rather than the bare `context.getFilesDir()` location. ([#1964](https://github.com/beeware/toga/issues/1964))
- GTK now returns `~/.local/state/appname/log` as the log file location, rather than `~/.cache/appname/log`. ([#1964](https://github.com/beeware/toga/issues/1964))
- The location returned by `toga.App.paths.app` is now the folder that contains the Python source file that defines the app class used by the app. If you are using a `toga.App` instance directly, this may alter the path that is returned. ([#1964](https://github.com/beeware/toga/issues/1964))
- On Winforms, if an application doesn't define an author, an author of `Unknown` is now used in application data paths, rather than `Toga`. ([#1964](https://github.com/beeware/toga/issues/1964))
- Winforms now returns `%USERPROFILE%/AppData/Local/<Author Name>/<App Name>/Data` as the user data file location, rather than `%USERPROFILE%/AppData/Local/<Author Name>/<App Name>`. ([#1964](https://github.com/beeware/toga/issues/1964))
- Support for SplitContainers with more than 2 panels of content has been removed. ([#1984](https://github.com/beeware/toga/issues/1984))
- Support for 3-tuple form of specifying SplitContainer items, used to prevent panels from resizing, has been removed. ([#1984](https://github.com/beeware/toga/issues/1984))
- The ability to increment and decrement the current OptionContainer tab was removed. Instead of *container.current_tab += 1*, use *container.current_tab = container.current_tab.index + 1* ([#1996](https://github.com/beeware/toga/issues/1996))
- `OptionContainer.add()`, `OptionContainer.remove()` and `OptionContainer.insert()` have been removed, due to being ambiguous with base widget methods of the same name. Use the `OptionContainer.content.append()`, `OptionContainer.content.remove()` and `OptionContainer.content.insert()` APIs instead. ([#1996](https://github.com/beeware/toga/issues/1996))
- The `on_select` handler for OptionContainer no longer receives the `option` argument providing the selected tab. Use `current_tab` to obtain the currently selected tab. ([#1996](https://github.com/beeware/toga/issues/1996))
- `TimePicker.min_time` and `TimePicker.max_time` has been renamed `TimeInput.min` and `TimeInput.max`, respectively. ([#1999](https://github.com/beeware/toga/issues/1999))
- `DatePicker.min_date` and `DatePicker.max_date` has been renamed `DateInput.min` and `DateInput.max`, respectively. ([#1999](https://github.com/beeware/toga/issues/1999))
- `NumberInput.min_value` and `NumberInput.max_value` have been renamed `NumberInput.min` and `NumberInput.max`, respectively. ([#1999](https://github.com/beeware/toga/issues/1999))
- `Slider.range` has been replaced by `Slider.min` and `Slider.max`. ([#1999](https://github.com/beeware/toga/issues/1999))
- Tables now use an empty string for the default missing value, rather than warning about missing values. ([#2011](https://github.com/beeware/toga/issues/2011))
- `Table.add_column()` has been deprecated in favor of `Table.append_column()` and `Table.insert_column()` ([#2011](https://github.com/beeware/toga/issues/2011))
- `Table.on_double_click` has been renamed `Table.on_activate`. ([#2011](https://github.com/beeware/toga/issues/2011), [#2017](https://github.com/beeware/toga/issues/2017))
- Trees now use an empty string for the default missing value, rather than warning about missing values. ([#2017](https://github.com/beeware/toga/issues/2017))
- The `parent` argument has been removed from the `insert` and `append` calls on `TreeSource`. This improves consistency between the API for `TreeSource` and the API for `list`. To insert or append a row in to a descendant of a TreeSource root, use `insert` and `append` on the parent node itself - i.e., `source.insert(parent, index, ...)` becomes `parent.insert(index, ...)`, and `source.insert(None, index, ...)` becomes `source.insert(index, ...)`. ([#2017](https://github.com/beeware/toga/issues/2017))
- When constructing a DetailedList from a list of tuples, or a list of lists, the required order of values has changed from (icon, title, subtitle) to (title, subtitle, icon). ([#2025](https://github.com/beeware/toga/issues/2025))
- The `on_select` handler for DetailedList no longer receives the selected row as an argument. ([#2025](https://github.com/beeware/toga/issues/2025))
- The handling of row deletion in DetailedList widgets has been significantly altered. The `on_delete` event handler has been renamed `on_primary_action`, and is now *only* a notification that a "swipe left" event (or platform equivalent) has been confirmed. This was previously inconsistent across platforms. Some platforms would update the data source to remove the row; some treated `on_delete` as a notification event and expected the application to handle the deletion. It is now the application's responsibility to perform the data deletion. ([#2025](https://github.com/beeware/toga/issues/2025))
- Support for Python 3.7 was removed. ([#2027](https://github.com/beeware/toga/issues/2027))
- `fill()` and `stroke()` now return simple drawing operations, rather than context managers. If you attempt to use `fill()` or `stroke()` on a context as a context manager, an exception will be raised; using these methods on Canvas will raise a warning, but return the appropriate context manager. ([#2029](https://github.com/beeware/toga/issues/2029))
- The `clicks` argument to `Canvas.on_press` has been removed. Instead, to detect "double clicks", you should use `Canvas.on_activate`. The `clicks` argument has also been removed from `Canvas.on_release`, `Canvas.on_drag`, `Canvas.on_alt_press`, `Canvas.on_alt_release`, and `Canvas.on_alt_drag`. ([#2029](https://github.com/beeware/toga/issues/2029))
- The `new_path` operation has been renamed `begin_path` for consistency with the HTML5 Canvas API. ([#2029](https://github.com/beeware/toga/issues/2029))
- Methods that generate new contexts have been renamed: `context()`, `closed_path()`, `fill()` and `stroke()` have become `Context()`, `ClosedPath()`, `Fill()` and `Stroke()` respectively. This has been done to make it easier to differentiate between primitive drawing operations and context-generating operations. ([#2029](https://github.com/beeware/toga/issues/2029))
- A Canvas is no longer implicitly a context object. The `Canvas.context` property now returns the root context of the canvas. If you were previously using `Canvas.context()` to generate an empty context, it should be replaced with `Canvas.Context()`. Any operations to `remove()` drawing objects from the canvas or `clear()` the canvas of drawing objects should be made on `Canvas.context`. Invoking these methods on `Canvas` will now call the base `Widget` implementations, which will throw an exception because `Canvas` widgets cannot have children. ([#2029](https://github.com/beeware/toga/issues/2029))
- The `preserve` option on `Fill()` operations has been deprecated. It was required for an internal optimization and can be safely removed without impact. ([#2029](https://github.com/beeware/toga/issues/2029))
- Drawing operations (e.g., `arc`, `line_to`, etc) can no longer be invoked directly on a Canvas. Instead, they should be invoked on the root context of the canvas, retrieved with via the *canvas* property. Context creating operations (`Fill`, `Stroke` and `ClosedPath`) are not affected. ([#2029](https://github.com/beeware/toga/issues/2029))
- The `tight` argument to `Canvas.measure_text()` has been deprecated. It was a GTK implementation detail, and can be safely removed without impact. ([#2029](https://github.com/beeware/toga/issues/2029))
- The `multiselect` argument to Open File and Select Folder dialogs has been renamed `multiple_select`, for consistency with other widgets that have multiple selection capability. ([#2058](https://github.com/beeware/toga/issues/2058))
- `Window.resizeable` and `Window.closeable` have been renamed `Window.resizable` and `Window.closable`, to adhere to US spelling conventions. ([#2058](https://github.com/beeware/toga/issues/2058))
- Windows no longer need to be explicitly added to the app's window list. When a window is created, it will be automatically added to the windows for the currently running app. ([#2058](https://github.com/beeware/toga/issues/2058))
- The optional arguments of `Command` and `Group` are now keyword-only. ([#2075](https://github.com/beeware/toga/issues/2075))
- In `App`, the properties `id` and `name` have been deprecated in favor of `app_id` and `formal_name` respectively, and the property `module_name` has been removed. ([#2075](https://github.com/beeware/toga/issues/2075))
- `GROUP_BREAK`, `SECTION_BREAK` and `CommandSet` were removed from the `toga` namespace. End users generally shouldn't need to use these classes. If your code *does* need them for some reason, you can access them from the `toga.command` namespace. ([#2075](https://github.com/beeware/toga/issues/2075))
- The `windows` constructor argument of `toga.App` has been removed. Windows are now automatically added to the current app. ([#2075](https://github.com/beeware/toga/issues/2075))
- The `filename` argument and property of `toga.Document` has been renamed `path`, and is now guaranteed to be a `pathlib.Path` object. ([#2075](https://github.com/beeware/toga/issues/2075))
- Documents must now provide a `create()` method to instantiate a `main_window` instance. ([#2075](https://github.com/beeware/toga/issues/2075))
- `App.exit()` now unconditionally exits the app, rather than confirming that the `on_exit` handler will permit the exit. ([#2075](https://github.com/beeware/toga/issues/2075))

### Documentation

- Documentation for application paths was added. ([#1849](https://github.com/beeware/toga/issues/1849))
- The contribution guide was expanded to include more suggestions for potential projects, and to explain how the backend tests work. ([#1868](https://github.com/beeware/toga/issues/1868))
- All code blocks were updated to add a button to copy the relevant contents on to the user's clipboard. ([#1897](https://github.com/beeware/toga/issues/1897))
- Class references were updated to reflect their preferred import location, rather than location where they are defined in code. ([#2001](https://github.com/beeware/toga/issues/2001))
- The Linux system dependencies were updated to reflect current requirements for developing and using Toga. ([#2021](https://github.com/beeware/toga/issues/2021))

### Misc

- [#1865](https://github.com/beeware/toga/issues/1865), [#1875](https://github.com/beeware/toga/issues/1875), [#1881](https://github.com/beeware/toga/issues/1881), [#1882](https://github.com/beeware/toga/issues/1882), [#1886](https://github.com/beeware/toga/issues/1886), [#1889](https://github.com/beeware/toga/issues/1889), [#1895](https://github.com/beeware/toga/issues/1895), [#1900](https://github.com/beeware/toga/issues/1900), [#1902](https://github.com/beeware/toga/issues/1902), [#1906](https://github.com/beeware/toga/issues/1906), [#1916](https://github.com/beeware/toga/issues/1916), [#1917](https://github.com/beeware/toga/issues/1917), [#1918](https://github.com/beeware/toga/issues/1918), [#1926](https://github.com/beeware/toga/issues/1926), [#1933](https://github.com/beeware/toga/issues/1933), [#1948](https://github.com/beeware/toga/issues/1948), [#1950](https://github.com/beeware/toga/issues/1950), [#1952](https://github.com/beeware/toga/issues/1952), [#1954](https://github.com/beeware/toga/issues/1954), [#1963](https://github.com/beeware/toga/issues/1963), [#1972](https://github.com/beeware/toga/issues/1972), [#1977](https://github.com/beeware/toga/issues/1977), [#1980](https://github.com/beeware/toga/issues/1980), [#1988](https://github.com/beeware/toga/issues/1988), [#1989](https://github.com/beeware/toga/issues/1989), [#1998](https://github.com/beeware/toga/issues/1998), [#2008](https://github.com/beeware/toga/issues/2008), [#2014](https://github.com/beeware/toga/issues/2014), [#2019](https://github.com/beeware/toga/issues/2019), [#2022](https://github.com/beeware/toga/issues/2022), [#2028](https://github.com/beeware/toga/issues/2028), [#2034](https://github.com/beeware/toga/issues/2034), [#2035](https://github.com/beeware/toga/issues/2035), [#2039](https://github.com/beeware/toga/issues/2039), [#2052](https://github.com/beeware/toga/issues/2052), [#2053](https://github.com/beeware/toga/issues/2053), [#2055](https://github.com/beeware/toga/issues/2055), [#2056](https://github.com/beeware/toga/issues/2056), [#2057](https://github.com/beeware/toga/issues/2057), [#2059](https://github.com/beeware/toga/issues/2059), [#2067](https://github.com/beeware/toga/issues/2067), [#2068](https://github.com/beeware/toga/issues/2068), [#2069](https://github.com/beeware/toga/issues/2069), [#2085](https://github.com/beeware/toga/issues/2085), [#2090](https://github.com/beeware/toga/issues/2090), [#2092](https://github.com/beeware/toga/issues/2092), [#2093](https://github.com/beeware/toga/issues/2093), [#2101](https://github.com/beeware/toga/issues/2101), [#2102](https://github.com/beeware/toga/issues/2102), [#2113](https://github.com/beeware/toga/issues/2113), [#2114](https://github.com/beeware/toga/issues/2114), [#2115](https://github.com/beeware/toga/issues/2115), [#2116](https://github.com/beeware/toga/issues/2116), [#2118](https://github.com/beeware/toga/issues/2118), [#2119](https://github.com/beeware/toga/issues/2119), [#2123](https://github.com/beeware/toga/issues/2123), [#2124](https://github.com/beeware/toga/issues/2124), [#2127](https://github.com/beeware/toga/issues/2127), [#2128](https://github.com/beeware/toga/issues/2128), [#2131](https://github.com/beeware/toga/issues/2131), [#2132](https://github.com/beeware/toga/issues/2132), [#2146](https://github.com/beeware/toga/issues/2146), [#2147](https://github.com/beeware/toga/issues/2147), [#2148](https://github.com/beeware/toga/issues/2148), [#2149](https://github.com/beeware/toga/issues/2149), [#2150](https://github.com/beeware/toga/issues/2150), [#2163](https://github.com/beeware/toga/issues/2163), [#2165](https://github.com/beeware/toga/issues/2165), [#2166](https://github.com/beeware/toga/issues/2166), [#2171](https://github.com/beeware/toga/issues/2171), [#2177](https://github.com/beeware/toga/issues/2177), [#2180](https://github.com/beeware/toga/issues/2180), [#2184](https://github.com/beeware/toga/issues/2184), [#2186](https://github.com/beeware/toga/issues/2186)

## 0.3.1 (2023-04-12)

### Features

- The Button widget now has 100% test coverage, and complete API documentation. ([#1761](https://github.com/beeware/toga/pull/1761))
- The mapping between Pack layout and HTML/CSS has been formalized. ([#1778](https://github.com/beeware/toga/pull/1778))
- The Label widget now has 100% test coverage, and complete API documentation. ([#1799](https://github.com/beeware/toga/pull/1799))
- TextInput now supports focus handlers and changing alignment on GTK. ([#1817](https://github.com/beeware/toga/pull/1817))
- The ActivityIndicator widget now has 100% test coverage, and complete API documentation. ([#1819](https://github.com/beeware/toga/pull/1819))
- The Box widget now has 100% test coverage, and complete API documentation. ([#1820](https://github.com/beeware/toga/pull/1820))
- NumberInput now supports changing alignment on GTK. ([#1821](https://github.com/beeware/toga/pull/1821))
- The Divider widget now has 100% test coverage, and complete API documentation. ([#1823](https://github.com/beeware/toga/pull/1823))
- The ProgressBar widget now has 100% test coverage, and complete API documentation. ([#1825](https://github.com/beeware/toga/pull/1825))
- The Switch widget now has 100% test coverage, and complete API documentation. ([#1832](https://github.com/beeware/toga/pull/1832))
- Event handlers have been internally modified to simplify their definition and use on backends. ([#1833](https://github.com/beeware/toga/pull/1833))
- The base Toga Widget now has 100% test coverage, and complete API documentation. ([#1834](https://github.com/beeware/toga/pull/1834))
- Support for FreeBSD was added. ([#1836](https://github.com/beeware/toga/pull/1836))
- The Web backend now uses Shoelace to provide web components. ([#1838](https://github.com/beeware/toga/pull/1838))
- Winforms apps can now go full screen. ([#1863](https://github.com/beeware/toga/pull/1863))

### Bugfixes

- Issues with reducing the size of windows on GTK have been resolved. ([#1205](https://github.com/beeware/toga/issues/1205))
- iOS now supports newlines in Labels. ([#1501](https://github.com/beeware/toga/issues/1501))
- The Slider widget now has 100% test coverage, and complete API documentation. ([#1708](https://github.com/beeware/toga/pull/1708))
- The GTK backend no longer raises a warning about the use of a deprecated `set_wmclass` API. ([#1718](https://github.com/beeware/toga/issues/1718))
- MultilineTextInput now correctly adapts to Dark Mode on macOS. ([#1783](https://github.com/beeware/toga/issues/1783))
- The handling of GTK layouts has been modified to reduce the frequency and increase the accuracy of layout results. ([#1794](https://github.com/beeware/toga/pull/1794))
- The text alignment of MultilineTextInput on Android has been fixed to be TOP aligned. ([#1808](https://github.com/beeware/toga/pull/1808))
- GTK widgets that involve animation (such as Switch or ProgressBar) are now redrawn correctly. ([#1826](https://github.com/beeware/toga/issues/1826))

### Improved Documentation

- API support tables now distinguish partial vs full support on each platform. ([#1762](https://github.com/beeware/toga/pull/1762))
- Some missing settings and constant values were added to the documentation of Pack. ([#1786](https://github.com/beeware/toga/pull/1786))
- Added documentation for `toga.App.widgets`. ([#1852](https://github.com/beeware/toga/pull/1852))

### Misc

- [#1750](https://github.com/beeware/toga/issues/1750), [#1764](https://github.com/beeware/toga/pull/1764), [#1765](https://github.com/beeware/toga/pull/1765), [#1766](https://github.com/beeware/toga/pull/1766), [#1770](https://github.com/beeware/toga/pull/1770), [#1771](https://github.com/beeware/toga/pull/1771), [#1777](https://github.com/beeware/toga/pull/1777), [#1797](https://github.com/beeware/toga/pull/1797), [#1802](https://github.com/beeware/toga/pull/1802), [#1813](https://github.com/beeware/toga/pull/1813), [#1818](https://github.com/beeware/toga/pull/1818), [#1822](https://github.com/beeware/toga/pull/1822), [#1829](https://github.com/beeware/toga/pull/1829), [#1830](https://github.com/beeware/toga/pull/1830), [#1835](https://github.com/beeware/toga/pull/1835), [#1839](https://github.com/beeware/toga/pull/1839), [#1854](https://github.com/beeware/toga/pull/1854), [#1861](https://github.com/beeware/toga/pull/1861)

## 0.3.0 (2023-01-30)

### Features

- Widgets now use a three-layered (Interface/Implementation/Native) structure.
- A GUI testing framework was added.
- A simplified "Pack" layout algorithm was added.
- Added a web backend.

### Bugfixes

- Too many to count!

## 0.2.15

- Added more widgets and cross-platform support, especially for GTK+ and Winforms

## 0.2.14

- Removed use of `namedtuple`

## 0.2.13

- Various fixes in preparation for PyCon AU demo

## 0.2.12

- Migrated to CSS-based layout, rather than Cassowary/constraint layout.
- Added Windows backend
- Added Django backend
- Added Android backend

## 0.2.0 - 0.2.11

Internal development releases.

## 0.1.2

- Further improvements to multiple-repository packaging strategy.
- Ensure Ctrl-C is honored by apps.
- **Cocoa:** Added runtime warnings when minimum OS X version is not met.

## 0.1.1

- Refactored code into multiple repositories, so that users of one backend don't have to carry the overhead of other installed platforms
- Corrected a range of bugs, mostly related to problems under Python 3.

## 0.1.0

Initial public release. Includes:

- A Cocoa (OS X) backend
- A GTK+ backend
- A proof-of-concept Win32 backend
- A proof-of-concept iOS backend
