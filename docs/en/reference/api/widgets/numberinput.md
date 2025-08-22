# NumberInput

A text input that is limited to numeric input.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/numberinput-cocoa.png" width="300"
alt="/reference/images/numberinput-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/numberinput-gtk.png" width="300"
alt="/reference/images/numberinput-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/numberinput-winforms.png" width="300"
alt="/reference/images/numberinput-winforms.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/numberinput-android.png" width="300"
alt="/reference/images/numberinput-android.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/numberinput-iOS.png" width="300"
alt="/reference/images/numberinput-iOS.png" />
</figure>
:::

::: {.group-tab}
Web [\|no\|](##SUBST##|no|)

Not supported
:::

::: {.group-tab}
Textual [\|no\|](##SUBST##|no|)

Not supported
:::
::::::::::

## Usage

``` python
import toga

widget = toga.NumberInput(min=1, max=10, step=0.001)
widget.value = 2.718
```

NumberInput's properties can accept `~decimal.Decimal`{.interpreted-text
role="class"}, `int`{.interpreted-text role="any"},
`float`{.interpreted-text role="any"}, or `str`{.interpreted-text
role="any"} containing numbers, but they always return
`~decimal.Decimal`{.interpreted-text role="class"} objects to ensure
precision is retained.

## Reference

::: {.autoclass}
toga.NumberInput
:::

::: {.autoprotocol}
toga.widgets.numberinput.OnChangeHandler
:::
