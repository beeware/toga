{{ component_header("DateInput", width=300) }}

## Usage

```python
import toga

current_date = toga.DateInput()
```

## Notes

- This widget supports years from 1800 to 8999 inclusive.
- Properties that return [`datetime.date`][] objects can also accept:
  - [`datetime.datetime`][]: The date portion will be extracted.
  - [`str`][]: Will be parsed as an ISO8601 format date string (e.g., "2023-12-25").
- On iOS, style directives for changing the widget's color and background color will be ignored. Apple advises against customizing the look and feel of date pickers; as a result, they don't expose APIs to change the color of date widgets.

## Reference

::: toga.DateInput

::: toga.widgets.dateinput.OnChangeHandler
