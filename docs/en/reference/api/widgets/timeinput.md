{{ component_header("TimeInput", width=300) }}

## Usage

```python
import toga

current_time = toga.TimeInput()
```

## Notes

- This widget supports hours, minutes and seconds. Microseconds will always be returned as zero.
    - On Android and iOS, seconds will also be returned as zero, and any second component of a minimum or maximum value will be ignored.
- On GTK3, GTK4, and libadwaita, the time is displayed in 24-hour format using separate native spin controls for hours, minutes, and seconds. GTK has no native time picker, so these controls provide native keyboard editing and accessibility. Values outside the minimum and maximum are clipped when an edit is committed.
- Properties that return [`datetime.time`][] objects can also accept:
    - [`datetime.datetime`][]: The time portion will be extracted.
    - [`str`][]: Will be parsed as an ISO8601 format time string (e.g., "06:12").

## Reference

::: toga.TimeInput

::: toga.widgets.timeinput.OnChangeHandler
