# Chroma Logging
### A wrapper for the standard python logging module to add color.

![Demo](docs/chroma_color.png)
![Demo](docs/chroma_uncolored.png)

## Installation
Chroma Logging is on PyPI and can be installed with:
```
pip install chromalogging
```

## Usage
Chroma Logging is works just like the regular logging module except
instead of a regular Formatter you use ChromaFormatter which takes a
boolean to determine whether or not to apply color, and another boolean
to determine whether to log in all bold.

```python
import sys
import chromalogging as logging

log = logging.getLogger()
log_format = logging.default_format_msg(levelname_min=6)
formatter = logging.ChromaFormatter(log_format, use_color=True, all_bold=True)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
log.addHandler(handler)
```

##### Custom Formatting
Alternatively custom format messages can be made. To use a color in a
log use $<COLOR_NAME_HERE> to add a color. $LEVEL or $Lto refer to the
color of the logging level for a log:
```python
log_format = ('$GREEN[%(asctime)-s]'
              '$LEVEL[%(levelname)-s]'
              '$MAGENTA[%(filename)-s:'
              '%(lineno)-d]$LEVEL: %(message)s')
```

All supported colors:

| Regular  | Light       |
| -------- | ----------- |
| $BLACK   | $LI_BLACK   |
| $RED     | $LI_RED     |
| $GREEN   | $LI_GREEN   |
| $YELLOW  | $LI_YELLOW  |
| $BLUE    | $LI_BLUE    |
| $MAGENTA | $LI_MAGENTA |
| $CYAN    | $LI_CYAN    |
| $WHITE   | $LI_WHITE   |

Additionally $BOLD or $B applies bold text and $RESET or $R resets back
to no colors or bold text.

All special codes:

| Verbose|Short Hand|
| ------ |--------- |
| $BOLD  | $B       |
| $RESET | $R       |
| $LEVEL | $L       |


#### Additional Configuration

ChromaFormatter has a dict called color_map to determine the colors of
other parts of the log msg. Logging levels, brackets and the colors of
formatted arguments are all set in color_map.

By default the colors are:

| Category | Color       |
| -------- | ----------- |
| DEBUG    | BLUE        |
| INFO     | Cyan        |
| WARNING  | YELLOW      |
| ERROR    | LIGHTRED_EX |
| CRITICAL | RED         |
| ARGS     | White       |
| BRACKETS | None        |

To change colors:
```python
formatter.color_map[logging.INFO] = logging.Fore.WHITE
formatter.color_map[logging.BRACKETS] = logging.Fore.RED
formatter.color_map[logging.ARGS] = logging.Fore.MAGENTA
```
Any colorama colors work here.
