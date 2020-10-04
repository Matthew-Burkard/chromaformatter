# Chroma Logging
### A wrapper to add color to the standard python logging module.

![Demo](docs/chroma_demo.png)

## Installation
Chroma Logging is on PyPI and can be installed with:
```
pip install chromalogging
```

## Usage
Chroma Logging adds two features to the default logging module, colors
can be added to the log format string, and formatted arguments in a log
message can be colored. The syntax to add colors in the format string is
```$COLOR_NAME_HERE``` to add a color. ```$LEVEL``` refers to the color
of the logging level for a log.
```python
log_format = ('$GREEN[%(asctime)-s]'
              '$LEVEL[%(levelname)-s]'
              '$MAGENTA[%(filename)-s:%(lineno)-d]'
              '$LEVEL: %(message)s')
```

To use, we use a chromalogging.ChromaFormatter rather than the
logging.Formatter.

```python
import sys
import chromalogging as logging

log = logging.getLogger()
log_format = ('$GREEN[%(asctime)-s]'
              '$LEVEL[%(levelname)-s]'
              '$MAGENTA[%(filename)-s:%(lineno)-d]'
              '$LEVEL: %(message)s')
formatter = logging.ChromaFormatter(log_format)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
log.addHandler(handler)
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

Additionally ```$BOLD``` applies bold text and ```$RESET``` resets back
to no colors unless ```use_bold``` is True, then it resets to bold text.

### Formatted Arguments in a Log
To apply color to a formatted argument in a log use ```{}``` as a
placeholder for arguments. ChromaFormatter will substitute ```{}``` with
any arguments passed in.
```python
log.info('Format {}.', 10)
```

### Additional Configuration
ChromaFormatter has a dict called ```color_map``` to determine the
colors of parts of the log msg that can't be configured from the format
string passed into ChromaFormatter. Logging levels and the color of
formatted arguments are set in color_map.

By default the colors are:

| Category | Color       |
| -------- | ----------- |
| DEBUG    | BLUE        |
| INFO     | Cyan        |
| WARNING  | YELLOW      |
| ERROR    | LIGHTRED_EX |
| CRITICAL | RED         |
| ARGS     | White       |

To change color_map colors use colorama:
```python
formatter.color_map[chromalogging.INFO] = colorama.Fore.WHITE
formatter.color_map[chromalogging.ARGS] = colorama.Fore.MAGENTA
```

## Applying to Existing Loggers
If you are using a third party module that uses the standard python
logging module you can apply a ChromaFormatter as such:
```python
import sys

import chromalogging as logging

log_format = logging.get_default_format_msg()
stream_formatter = logging.ChromaFormatter(log_format)
stream_handler = logging.StreamHandler(stream=sys.stdout)

flask_logger = logging.getLogger('werkzeug')
while flask_logger.handlers:
    flask_logger.removeHandler(flask_logger.handlers.pop())
flask_logger.addHandler(stream_handler)
```
