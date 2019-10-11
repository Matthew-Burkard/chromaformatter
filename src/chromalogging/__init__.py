import re
from logging import *

from sty import fg, rs, ef


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
    RESET = rs.all


RESET_SEQ = rs.all
BOLD_SEQ = ef.bold
ARGS = -10
BRACKET = -20

color_map = {
    DEBUG: Colors.LI_BLUE,
    INFO: Colors.WHITE,
    WARNING: Colors.YELLOW,
    ERROR: Colors.LI_RED,
    CRITICAL: Colors.RED,
    ARGS: Colors.RESET,
    BRACKET: Colors.GREEN
}

_COLOR_INPUT = '{}'
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

    def __init__(self, msg, use_color, all_bold=False):
        self.use_color = use_color
        self.all_bold = BOLD_SEQ if all_bold else ''
        msg = _formatter_message(msg, use_color, self.all_bold)
        super().__init__(msg)

    def format(self, record):
        # noinspection PyTypeChecker
        _init_record(record)
        if not self.use_color or record.levelno not in color_map:
            record.msg = re.sub(r'{}', '[%s]', record.msg)
            return Formatter.format(self, record)
        bc = color_map[BRACKET] + self.all_bold
        ac = color_map[ARGS] + self.all_bold
        lc = color_map[record.levelno] + self.all_bold
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


def _formatter_message(msg, use_color, all_bold):
    if use_color:
        msg = f'{all_bold}{msg}$RESET'
        msg = _adjust_format_lengths(msg, use_color, all_bold)
        msg = re.sub(r'\$(RESET|R)', RESET_SEQ + all_bold, msg)
        msg = re.sub(r'\$(BOLD|B)', BOLD_SEQ, msg)
        for color_word, color in _COLOR_WORD_TO_COLOR.items():
            msg = msg.replace(f'${color_word}', color + all_bold)
    else:
        msg = re.sub(r'\$[A-Z_]+\b', '', msg)
    return msg


def _adjust_format_lengths(msg, use_color, all_bold):
    length_search = re.search(r'%\(levelname\)-([0-9]+)s', msg)
    if not length_search:
        return msg
    length = int(length_search.group(1))
    length += 9 if use_color else 0
    length += 4 if all_bold else 0
    msg = re.sub(r'%\((levelname)\)-([0-9]+)s', fr'%(\1)-{length}s', msg)
    return msg
