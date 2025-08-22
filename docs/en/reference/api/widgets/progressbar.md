# ProgressBar

A horizontal bar to visualize task progress. The task being monitored
can be of known or indeterminate length.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/progressbar-cocoa.png" width="300"
alt="/reference/images/progressbar-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/progressbar-gtk.png" width="300"
alt="/reference/images/progressbar-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/progressbar-winforms.png" width="300"
alt="/reference/images/progressbar-winforms.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/progressbar-android.png" width="300"
alt="/reference/images/progressbar-android.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/progressbar-iOS.png" width="300"
alt="/reference/images/progressbar-iOS.png" />
</figure>
:::

::: {.group-tab}
Web [\|beta\|](##SUBST##|beta|)

<figure class="align-center">
<img src="/reference/images/progressbar-web.png" width="300"
alt="/reference/images/progressbar-web.png" />
</figure>
:::

::: {.group-tab}
Textual [\|no\|](##SUBST##|no|)

Not supported
:::
::::::::::

## Usage

If a progress bar has a `max` value, it is a *determinate* progress bar.
The value of the progress bar can be altered over time, indicating
progress on a task. The visual indicator of the progress bar will be
filled indicating the proportion of `value` relative to `max`. `max` can
be any positive numerical value.

``` python
import toga

progress = toga.ProgressBar(max=100, value=1)

# Start progress animation
progress.start()

# Update progress to 10%
progress.value = 10

# Stop progress animation
progress.stop()
```

If a progress bar does *not* have a `max` value (i.e., `max == None`),
it is an *indeterminate* progress bar. Any change to the value of an
indeterminate progress bar will be ignored. When started, an
indeterminate progress bar animates as a throbbing or "ping pong"
animation.

``` python
import toga

progress = toga.ProgressBar(max=None)

# Start progress animation
progress.start()

# Stop progress animation
progress.stop()
```

## Notes

- The visual appearance of progress bars varies from platform to
  platform. Toga will try to provide a visual distinction between
  running and not-running determinate progress bars, but this cannot be
  guaranteed.

## Reference

::: {.autoclass}
toga.ProgressBar
:::
