{{ component_header("Pack") }}

## Usage

Toga's default style engine, **Pack**, is a layout algorithm based around the idea of packing boxes inside boxes. Each box specifies a direction for its children, and each child specifies how it will consume the available space - either as a specific width, or as a proportion of the available width. Other properties exist to control color, text alignment and so on.

It is similar in some ways to the CSS Flexbox algorithm; but dramatically simplified, as there is no allowance for overflowing boxes.

The string values defined here are the string literals that the Pack algorithm accepts. These values are also pre-defined as Python constants in the `toga.style.pack` module with the same name; however, following Python style, the constants use upper case and dashes are underscores. For example, the Python constant `toga.style.pack.SANS_SERIF` evaluates as the string literal `"sans-serif"`. (The constant `NONE`, or `"none"`, is distinct from Python's `None`.)

Some properties, despite always storing their value in a consistent form, are more liberal in what they accept, and will convert as necessary when assigned alternate forms. Where relevant, these are listed under **Accepts**.

Toga has a [layout debug mode][debug-layout] to aid in visually debugging or exploring Pack layouts.


## Reference

::: toga.style.pack.Pack
    options:
      show_bases: false
      merge_init_into_class: false
      members_order: source

## The relationship between Pack and CSS

Pack aims to be a functional subset of CSS. Any Pack layout can be converted into an equivalent CSS layout. After applying this conversion, the CSS layout should be considered a "reference implementation". Any disagreement between the rendering of a converted Pack layout in a browser, and the layout produced by the Toga implementation of Pack should be considered to be either a bug in Toga, or a bug in the mapping.

The mapping that can be used to establish the reference implementation is:

- The reference HTML layout document is rendered in [no-quirks mode](https://developer.mozilla.org/en-US/docs/Web/HTML/Quirks_Mode_and_Standards_Mode), with a default CSS stylesheet:

```html
<!DOCTYPE html>
<html>
    <head>
       <meta charset="UTF-8" />
       <title>Pack layout testbed</title>
       <style>
          html, body {
             height: 100%;
          }
          body {
             overflow: hidden;
             display: flex;
             margin: 0;
             white-space: pre;
          }
          div {
             display: flex;
             white-space: pre;
          }
       </style>
    </head>
    <body></body>
</html>
```

- The root widget of the Pack layout can be mapped to the `<body>` element of the HTML reference document. The rendering area of the browser window becomes the view area that Pack will fill.

- ImageViews map to `<img>` elements. The `<img>` element has an additional style of `object-fit: contain` unless *both* `height` and `width` are defined.

- All other widgets are mapped to `<div>` elements.

- The following Pack declarations can be mapped to equivalent CSS declarations:

| Pack property           | CSS property                                                                                                                         |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `direction: <str>`      | `flex-direction: <str>`                                                                                                              |
| `display: pack`         | `display: flex`                                                                                                                      |
| `flex: <int>`           | If `direction == "row"` and `width` is set, or `direction == "column"` and `height` is set, ignore. Otherwise, `flex: <int> 0 auto`. |
| `font_size: <int>`      | `font-size: <int>pt`                                                                                                                 |
| `height: <value>`       | `height: <value>px` if value is an integer; `height: auto` if value is `"none"`.                                                     |
| `margin_top: <int>`     | `margin-top: <int>px`                                                                                                                |
| `margin_bottom: <int>`  | `margin-bottom: <int>px`                                                                                                             |
| `margin_left: <int>`    | `margin-left: <int>px`                                                                                                               |
| `margin_right: <int>`   | `margin-right: <int>px`                                                                                                              |
| `text_direction: <str>` | `direction: <str>`                                                                                                                   |
| `width: <value>`        | `width: <value>px` if value is an integer; `width: auto` if value is `"none"`.                                                       |

- All other Pack declarations should be used as-is as CSS declarations, with underscores being converted to dashes (e.g., `background_color` becomes `background-color`).
