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
Chroma Logging is designed work just like the regular logging module
except instead of a regular Formatter you use ChromaFormatter which
takes a boolean to determine whether or not to apply color, and another
boolean to determine whether to log in all bold.

To use a color in a log place $<COLOR_NAME_HERE> or $LEVEL to refer to
the color of the logging level for a log:
```python
import sys
import chromalogging as logging

log = logging.getLogger()
log_format = ('$GREEN[%(asctime)-s]'
              '$LEVEL[%(levelname)-s$LEVEL]'
              '$MAGENTA[%(filename)-s:'
              '%(lineno)-d]$LEVEL: %(message)s')
formatter = logging.ChromaFormatter(log_format, use_color=True, all_bold=True)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
log.addHandler(handler)
```

Alternatively there is a default log msg that can be used.
```python
log_format = logging.default_format_msg(levelname_min=6)
```

Additionally $BOLD or $B applies bold text and $RESET or $R resets back
to no colors or bold text.

#### Configuration

By default the logging level colors are:
- DEBUG: Fore.BLUE
- INFO: Fore.Cyan
- WARNING: Fore.YELLOW
- ERROR: Fore.LIGHTRED_EX
- CRITICAL: Fore.RED

Formatted arguments will be surrounded by brackets and have configurable
colors.

Colors can be changed as such:
```python
logging.color_map[logging.INFO] = logging.Fore.WHITE
logging.color_map[logging.BRACKET] = logging.Fore.RED
logging.color_map[logging.ARGS] = logging.Fore.MAGENTA
```
Any colorama colors work.
