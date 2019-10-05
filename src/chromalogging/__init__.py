import re
from logging import *

from sty import fg, rs, ef

_COLOR_INPUT = '{}'

all_bold = False
RESET_SEQ = rs.all
BOLD_SEQ = ef.bold
ARGS = -10
BRACKET = -20


class Colors:
    BLACK = fg.black
    RED = fg.red
    LI_RED = fg.li_red
    GREEN = fg.green
    YELLOW = fg.yellow
    LI_BLUE = fg.li_blue
    BLUE = fg.blue
    MAGENTA = fg.magenta
    CYAN = fg.cyan
    WHITE = fg.white
    RESET = RESET_SEQ


color_map = {
    DEBUG: Colors.LI_BLUE,
    INFO: Colors.WHITE,
    WARNING: Colors.YELLOW,
    ERROR: Colors.LI_RED,
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


class ChromaFormatter(Formatter):

    def __init__(self, msg, use_color):
        self.use_color = use_color
        msg = _formatter_message(msg, use_color)
        super().__init__(msg)

    def format(self, record):
        # noinspection PyTypeChecker
        _init_record(record)
        if not self.use_color or record.levelno not in color_map:
            record.msg = re.sub(r'{}', '[%s]', record.msg)
            return Formatter.format(self, record)
        bc = color_map[BRACKET] + _b()
        ac = color_map[ARGS] + _b()
        lc = color_map[record.levelno] + _b()
        record.msg = lc + record.msg
        if record.args:
            record.msg = re.sub(r'{}', f'{bc}[{ac}%s{bc}]{lc}', record.msg)
        record.levelname = f'{lc}{record.levelname}{RESET_SEQ}'
        return Formatter.format(self, record)


def _init_record(record):
    record.msg = str(record.msg)
    try:
        if record.consumed:
            record.msg = record.original_msg
            record.levelname = record.original_lvl
            record.args = record.original_args
    except AttributeError:
        record.original_msg = record.msg
        record.original_lvl = record.levelname
        record.original_args = record.args
        record.consumed = True


def _formatter_message(msg, use_color):
    if use_color:
        msg = f'{_b()}{msg}$RESET'
        msg = re.sub(r'\$(RESET|R)', RESET_SEQ + _b(), msg)
        msg = re.sub(r'\$(BOLD|B)', BOLD_SEQ, msg)
        for color_word, color in _COLOR_WORD_TO_COLOR.items():
            msg = msg.replace(f'${color_word}', color + _b())
    else:
        msg = re.sub(r'\$[A-Z_]+\b', '', msg)
    return msg


def _b():
    return BOLD_SEQ if all_bold else ''
