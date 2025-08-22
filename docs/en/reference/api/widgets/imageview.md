# ImageView

A widget that displays an image.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/imageview.png" width="150"
alt="/reference/images/imageview.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/imageview.png" width="150"
alt="/reference/images/imageview.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/imageview.png" width="150"
alt="/reference/images/imageview.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/imageview.png" width="150"
alt="/reference/images/imageview.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/imageview.png" width="150"
alt="/reference/images/imageview.png" />
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

An `~toga.ImageView`{.interpreted-text role="class"} provides a
mechanism to display an `~toga.Image`{.interpreted-text role="class"} as
part of an interface.

``` python
import toga

my_image = toga.Image(self.paths.app / "brutus.png")
view = toga.ImageView(my_image)
```

## Notes

- An ImageView **is not** an interactive element - there is no
  `on_press` handler for ImageView. If you want a graphical element that
  can be clicked or pressed, try using a `toga.Button`{.interpreted-text
  role="any"} that uses an `toga.Icon`{.interpreted-text role="any"}.
- The default size of the view is the size of the image, or 0x0 if
  `image` is `None`.
- If an explicit width *or* height is specified, the size of the image
  will be fixed in that axis, and the size in the other axis will be
  determined by the image's aspect ratio.
- If an explicit width *and* height is specified, the image will be
  scaled to fill the described size without preserving the aspect ratio.
- If an ImageView is given a style of `flex=1`, and doesn't have an
  explicit size set along its container's main axis, it will be allowed
  to expand and contract along that axis, with the size determined by
  the flex allocation.
  - If the cross axis size is unspecified, it will be determined by
    applying the image's aspect ratio to the size allocated on the main
    axis.
  - If the cross axis has an explicit size, the image will be scaled to
    fill the available space so that the entire image can be seen, while
    preserving its aspect ratio. Any extra space will be distributed
    equally between both sides.

## Reference

::: {.autoclass}
toga.ImageView
:::
