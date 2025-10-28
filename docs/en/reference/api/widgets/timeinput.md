# TimeInput

A widget to select a clock time.

/// tab | macOS

![/reference/images/timeinput-cocoa.png](/reference/images/timeinput-cocoa.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux {{ not_supported }}

Not supported

///

/// tab | Windows

![/reference/images/timeinput-winforms.png](/reference/images/timeinput-winforms.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/timeinput-android.png](/reference/images/timeinput-android.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/timeinput-iOS.png](/reference/images/timeinput-iOS.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Web {{ not_supported }}

![/reference/images/timeinput-web.png](/reference/images/timeinput-web.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Textual {{ not_supported }}

Not supported

///

## Usage

```python
import toga

current_time = toga.TimeInput()
```

## Notes

- This widget supports hours, minutes and seconds. Microseconds will always be returned as zero.
    - On Android and iOS, seconds will also be returned as zero, and any second component of a minimum or maximum value will be ignored.
- Properties that return [`datetime.time`][] objects can also accept:
    - [`datetime.datetime`][]: The time portion will be extracted.
    - [`str`][]: Will be parsed as an ISO8601 format time string (e.g., "06:12").

## Reference

::: toga.TimeInput

::: toga.widgets.timeinput.OnChangeHandler
