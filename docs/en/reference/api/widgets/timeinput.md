{{ component_header("TimeInput", width=300) }}

## Usage

```python
import toga

current_time = toga.TimeInput()
```

## Notes

- This widget supports hours, minutes and seconds. Microseconds will always be returned as zero.
  - On Android and iOS, seconds will also be returned as zero, and any second component of a minimum or maximum value will be ignored.
- Properties that return [`datetime.time`][] objects can also accept:
  - [`datetime.datetime`][]: The time portion will be extracted.
  - [`str`][]: Will be parsed as an ISO8601 format time string (e.g., "06:12").

## Reference

::: toga.TimeInput

::: toga.widgets.timeinput.OnChangeHandler
