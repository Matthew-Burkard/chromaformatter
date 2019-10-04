import re
from logging import *

from sty import fg, rs, ef

_COLOR_INPUT = '{}'
_LIGHT = True

RESET_SEQ = rs.all
BOLD_SEQ = ef.bold
ARGS = -10
BRACKET = -20


class Colors:
    BLACK = fg.black
    RED = fg.li_red if _LIGHT else fg.red
    GREEN = fg.green
    YELLOW = fg.yellow
    BLUE = fg.li_blue if _LIGHT else fg.blue
    MAGENTA = fg.magenta
    CYAN = fg.cyan
    WHITE = fg.white
    RESET = RESET_SEQ


COLOR_MAP = {
    DEBUG: Colors.BLUE,
    INFO: Colors.WHITE,
    WARNING: Colors.YELLOW,
    ERROR: Colors.RED,
    CRITICAL: Colors.RED,
    ARGS: Colors.RESET,
    BRACKET: Colors.GREEN
}

_COLOR_WORD_TO_COLOR = {
    'BLACK': Colors.BLACK,
    'RED': Colors.RED,
    'GREEN': Colors.GREEN,
    'YELLOW': Colors.YELLOW,
    'BLUE': Colors.BLUE,
    'MAGENTA': Colors.MAGENTA,
    'CYAN': Colors.CYAN,
    'WHITE': Colors.WHITE,
    'RESET': Colors.RESET
}


def _formatter_message(msg, use_color):
    if use_color:
        msg = msg.replace('$RESET', RESET_SEQ).replace('$BOLD', BOLD_SEQ)
        for color_word, color in _COLOR_WORD_TO_COLOR.items():
            msg = msg.replace(f'${color_word}', color)
    else:
        msg = msg.replace('$RESET', '').replace('$BOLD', '')
    return msg


class ColoredFormatter(Formatter):

    def __init__(self, msg, use_color):
        msg = _formatter_message(msg, use_color)
        Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        record.msg = str(record.msg)
        if record.levelno not in COLOR_MAP:
            return Formatter.format(self, record)
        bc = COLOR_MAP[BRACKET]
        ac = COLOR_MAP[ARGS]
        lc = COLOR_MAP[record.levelno]
        record.msg = lc + record.msg
        if record.args:
            record.msg = re.sub(r'{}', f'{bc}[{ac}%s{bc}]{lc}', record.msg)
        record.levelname = f'{lc}{record.levelname}{RESET_SEQ}'
        return Formatter.format(self, record)
