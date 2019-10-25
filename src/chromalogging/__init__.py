import re
from logging import *

from colorama import init, Fore, Back, Style

init()

ARGS = -10
BRACKET = -20

RESET = Fore.RESET + Back.RESET
BOLD = Style.BRIGHT

color_map = {
    DEBUG: Fore.BLUE,
    INFO: Fore.CYAN,
    WARNING: Fore.YELLOW,
    ERROR: Fore.LIGHTRED_EX,
    CRITICAL: Fore.RED,
    ARGS: Fore.WHITE,
    BRACKET: RESET
}

_COLOR_INPUT = '{}'
_COLOR_WORD_TO_COLOR = {
    'BLACK': Fore.BLACK,
    'RED': Fore.RED,
    'GREEN': Fore.GREEN,
    'YELLOW': Fore.YELLOW,
    'BLUE': Fore.BLUE,
    'MAGENTA': Fore.MAGENTA,
    'CYAN': Fore.CYAN,
    'WHITE': Fore.WHITE,
    'RESET': Fore.RESET,
    'LI_BLACK': Fore.LIGHTBLACK_EX,
    'LI_RED': Fore.LIGHTRED_EX,
    'LI_GREEN': Fore.LIGHTGREEN_EX,
    'LI_YELLOW': Fore.LIGHTYELLOW_EX,
    'LI_BLUE': Fore.LIGHTBLUE_EX,
    'LI_MAGENTA': Fore.LIGHTMAGENTA_EX,
    'LI_CYAN': Fore.LIGHTCYAN_EX,
    'LI_WHITE': Fore.LIGHTWHITE_EX
}


class ChromaFormatter(Formatter):
    """Extends logging.Formatter to add colors and styles"""

    def __init__(self, msg, use_color, all_bold=False):
        """Create an instance of ChromaFormatter.

        :param msg: The format string to determine how logs will
        appear.
        :type msg: str

        :param use_color: Colors will be applied if True.
        :type use_color: bool

        :param all_bold: Whole log will be bold if True, defaults to
        False.
        :type all_bold: bool
        """
        self.use_color = use_color
        self.all_bold = BOLD if all_bold else ''
        msg = _process_format_message(msg, use_color, self.all_bold)
        super().__init__(msg)

    def format(self, record):
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
    """Makes certain a LogRecord will be using it's original values.

    :param record: LogRecord to load with initial values.
    :type record: LogRecord

    First time called with will add original values to a LogRecord,
    as new parameters. Subsequent calls will reset a LogRecords
    parameters back ot the originals.

    This is so that other handlers won't have the colors inserted from
    previous ones.
    """
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


def _process_format_message(msg, use_color, all_bold):
    """Applies colors and styles where needed.

    :param msg: msg to format.
    :type msg: str

    :param use_color: Color words in msg will be replaced by colors if
    True else they will be replaced with empty strings.
    :type use_color: bool

    :param all_bold: Each color will be that color + bold if True.
    :type all_bold: bool

    :return: The processed msg.
    :rtype: str
    """
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
    """Adjusts format lengths to account for the length of color codes.

    :param msg: Original msg
    :type msg: str

    :param use_color: To know what adjustments need to be made.
    :type use_color: bool

    :param all_bold: To know what adjustments need to be made.
    :type all_bold: bool

    :return: msg with new formatted lengths.
    :rtype: str
    """
    length_search = re.search(r'%\(levelname\)-([0-9]+)s', msg)
    if not length_search:
        return msg
    length = int(length_search.group(1))
    length += len(Fore.WHITE) * 3 if use_color else 0
    length += len(Style.BRIGHT) if all_bold else 0
    msg = re.sub(r'%\((levelname)\)-([0-9]+)s', fr'%(\1)-{length}s', msg)
    return msg
