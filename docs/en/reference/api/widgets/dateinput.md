# DateInput

A widget to select a calendar date.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/dateinput-cocoa.png" width="300"
alt="/reference/images/dateinput-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux [\|no\|](##SUBST##|no|)

Not supported
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/dateinput-winforms.png" width="300"
alt="/reference/images/dateinput-winforms.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/dateinput-android.png" width="300"
alt="/reference/images/dateinput-android.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/dateinput-iOS.png" width="300"
alt="/reference/images/dateinput-iOS.png" />
</figure>
:::

::: {.group-tab}
Web

<figure class="align-center">
<img src="/reference/images/dateinput-web.png" width="300"
alt="/reference/images/dateinput-web.png" />
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

current_date = toga.DateInput()
```

## Notes

- This widget supports years from 1800 to 8999 inclusive.
- Properties that return `datetime.date`{.interpreted-text role="any"}
  objects can also accept:
  - `datetime.datetime`{.interpreted-text role="any"}: The date portion
    will be extracted.
  - `str`{.interpreted-text role="any"}: Will be parsed as an ISO8601
    format date string (e.g., "2023-12-25").
- On iOS, style directives for changing the widget's color and
  background color will be ignored. Apple advises against customizing
  the look and feel of date pickers; as a result, they don't expose APIs
  to change the color of date widgets.

## Reference

::: {.autoclass}
toga.DateInput
:::

::: {.autoprotocol}
toga.widgets.dateinput.OnChangeHandler
:::
