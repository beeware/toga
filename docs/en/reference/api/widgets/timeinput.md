# TimeInput

A widget to select a clock time.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/timeinput-cocoa.png" width="300"
alt="/reference/images/timeinput-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux [\|no\|](##SUBST##|no|)

Not supported
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/timeinput-winforms.png" width="300"
alt="/reference/images/timeinput-winforms.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/timeinput-android.png" width="300"
alt="/reference/images/timeinput-android.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/timeinput-iOS.png" width="300"
alt="/reference/images/timeinput-iOS.png" />
</figure>
:::

::: {.group-tab}
Web [\|no\|](##SUBST##|no|)

<figure class="align-center">
<img src="/reference/images/timeinput-web.png" width="300"
alt="/reference/images/timeinput-web.png" />
</figure>
:::

::: {.group-tab}
Textual [\|no\|](##SUBST##|no|)

Not supported
:::
::::::::::

## Usage

``` python
import toga

current_time = toga.TimeInput()
```

## Notes

- This widget supports hours, minutes and seconds. Microseconds will
  always be returned as zero.
  - On Android and iOS, seconds will also be returned as zero, and any
    second component of a minimum or maximum value will be ignored.
- Properties that return `datetime.time`{.interpreted-text role="any"}
  objects can also accept:
  - `datetime.datetime`{.interpreted-text role="any"}: The time portion
    will be extracted.
  - `str`{.interpreted-text role="any"}: Will be parsed as an ISO8601
    format time string (e.g., "06:12").

## Reference

::: {.autoclass}
toga.TimeInput
:::

::: {.autoprotocol}
toga.widgets.timeinput.OnChangeHandler
:::
