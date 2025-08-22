# ActivityIndicator

A small animated indicator showing activity on a task of indeterminate
length, usually rendered as a "spinner" animation.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/activityindicator-cocoa.png" width="100"
alt="/reference/images/activityindicator-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/activityindicator-gtk.png" width="100"
alt="/reference/images/activityindicator-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/activityindicator-winforms.png" width="100"
alt="/reference/images/activityindicator-winforms.png" />
</figure>
:::

::: {.group-tab}
Android [\|no\|](##SUBST##|no|)

Not supported
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/activityindicator-iOS.png" width="100"
alt="/reference/images/activityindicator-iOS.png" />
</figure>
:::

::: {.group-tab}
Web [\|beta\|](##SUBST##|beta|)

<figure class="align-center">
<img src="/reference/images/activityindicator-web.png" width="100"
alt="/reference/images/activityindicator-web.png" />
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

indicator = toga.ActivityIndicator()

# Start the animation
indicator.start()

# Stop the animation
indicator.stop()
```

## Notes

- The ActivityIndicator will always take up a fixed amount of physical
  space in a layout. However, the widget will not be visible when it is
  in a "stopped" state.

## Reference

::: {.autoclass}
toga.ActivityIndicator
:::
