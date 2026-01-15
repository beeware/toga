{{ component_header("Color") }}

## Usage

When specifying colors for style properties such as [color][toga.style.pack.Pack.color] and [background-color][toga.style.pack.Pack.background_color], or on widget APIs that use colors explicitly (such as any `color` arguments for the [`Canvas`](../widgets/canvas.md) API), Toga will accept values in a [range of possible formats][toga.colors.ColorT].

## Reference

::: toga.colors.ColorT

::: toga.colors.Color
	options:
		members: [rgb, hsl]
		show_signature_annotations: false

::: toga.colors.rgb
	options:
		members: [r, g, b, a]
		inherited_members: [a]

::: toga.colors.hsl
	options:
		members: [h, s, l, a]
		inherited_members: [a]
