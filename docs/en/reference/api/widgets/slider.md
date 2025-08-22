# Slider

A widget for selecting a value within a range. The range is shown as a
horizontal line, and the selected value is shown as a draggable marker.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/slider-cocoa.png" width="300"
alt="/reference/images/slider-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/slider-gtk.png" width="300"
alt="/reference/images/slider-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/slider-winforms.png" width="300"
alt="/reference/images/slider-winforms.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/slider-android.png" width="300"
alt="/reference/images/slider-android.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/slider-iOS.png" width="300"
alt="/reference/images/slider-iOS.png" />
</figure>
:::

::: {.group-tab}
Web

<figure class="align-center">
<img src="/reference/images/slider-web.png" width="300"
alt="/reference/images/slider-web.png" />
</figure>
:::

::: {.group-tab}
Textual [\|no\|](##SUBST##|no|)

Not supported
:::
::::::::::

## Usage

A slider can either be continuous (allowing any value within the range),
or discrete (allowing a fixed number of equally-spaced values). For
example:

``` python
import toga

def my_callback(slider):
    print(slider.value)

# Continuous slider, with an event handler.
toga.Slider(min=-5, max=10, value=7, on_change=my_callback)

# Discrete slider, accepting the values [0, 1.5, 3, 4.5, 6, 7.5].
toga.Slider(min=0, max=7.5, tick_count=6)
```

## Reference

::: {.autoclass}
toga.Slider
:::

::: {.autoprotocol}
toga.widgets.slider.OnChangeHandler
:::

::: {.autoprotocol}
toga.widgets.slider.OnPressHandler
:::

::: {.autoprotocol}
toga.widgets.slider.OnReleaseHandler
:::
