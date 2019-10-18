import re
from logging import *

from chromalogging.ansi import *

ARGS = -10
BRACKET = -20

color_map = {
    DEBUG: LI_BLUE,
    INFO: WHITE,
    WARNING: YELLOW,
    ERROR: LI_RED,
    CRITICAL: RED,
    ARGS: CYAN,
    BRACKET: RESET
}

_COLOR_INPUT = '{}'
_COLOR_WORD_TO_COLOR = {
    'BLACK': BLACK,
    'RED': RED,
    'GREEN': GREEN,
    'YELLOW': YELLOW,
    'BLUE': BLUE,
    'MAGENTA': MAGENTA,
    'CYAN': CYAN,
    'WHITE': WHITE,
    'RESET': RESET,
    'LI_BLACK': LI_BLACK,
    'LI_RED': LI_RED,
    'LI_GREEN': LI_GREEN,
    'LI_YELLOW': LI_YELLOW,
    'LI_BLUE': LI_BLUE,
    'LI_MAGENTA': LI_MAGENTA,
    'LI_CYAN': LI_CYAN,
    'LI_WHITE': LI_WHITE,
}


class ChromaFormatter(Formatter):

    def __init__(self, msg, use_color, all_bold=False):
        self.use_color = use_color
        self.all_bold = BOLD if all_bold else ''
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
        record.levelname = f'{lc}{record.levelname}{RESET}'
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
        msg = re.sub(r'\$(RESET|R(?!ED))', RESET + all_bold, msg)
        msg = re.sub(r'\$(BOLD|B(?!LUE|LACK))', BOLD, msg)
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
