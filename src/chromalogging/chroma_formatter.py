import re
from typing import Dict, Any

from colorama import Fore, Style

from chromalogging import (Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL,
                           LogRecord)

ARGS = -10
BRACKETS = -20

RESET = Style.RESET_ALL
BOLD = Style.BRIGHT

_WORD_TO_COLOR: Dict[str, str] = {
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


# noinspection PyProtectedMember
class ChromaFormatter(Formatter):
    """Extends logging.Formatter to add colors and styles."""

    def __init__(self, msg: str, use_color: bool = True,
                 all_bold: bool = True) -> None:
        """Set ChromaFormatter properties.

        :param msg: The format string to determine how logs will appear.
        :param use_color: Colors will be applied if True, defaults to
            True.
        :param all_bold: Whole log will be bold if True, defaults to
            True.
        """
        self.use_color: bool = use_color
        self.add_brackets_to_args: bool = True
        self._bold: str = BOLD if all_bold else ''
        msg = _format_message(msg, use_color, self._bold)
        super().__init__(msg)
        if use_color:
            self._original_style_fmt = self._style._fmt

        self.color_map: Dict[int, Any] = {
            DEBUG: Fore.BLUE,
            INFO: Fore.CYAN,
            WARNING: Fore.YELLOW,
            ERROR: Fore.LIGHTRED_EX,
            CRITICAL: Fore.RED,
            ARGS: Fore.WHITE,
            BRACKETS: ''
        }

    def format(self, record: LogRecord) -> str:
        _init_record(record)
        if not self.use_color or record.levelno not in self.color_map:
            replace = '[%s]' if self.add_brackets_to_args else '%s'
            record.msg = re.sub(r'(?<!{){}(?!})', replace, record.msg)
            return Formatter.format(self, record)
        self._style._fmt = self._original_style_fmt
        if self._bold:
            self._style._fmt = re.sub(re.escape(BOLD), '', self._style._fmt)
            self._style._fmt = BOLD + self._style._fmt
        # Shorthands for different colors.
        bc = self.color_map[BRACKETS] + self._bold
        ac = self.color_map[ARGS] + self._bold
        lc = self.color_map[record.levelno] + self._bold
        if self.color_map[BRACKETS]:
            self._color_brackets(bc)
        record.msg = lc + record.msg
        if record.args:
            record.msg = re.sub(r'(?<!{){}(?!})',
                                f'{ac}{bc}[{ac}%s{bc}]{lc}'
                                if self.add_brackets_to_args else
                                f'{ac}%s{lc}', record.msg)
        self._style._fmt = re.sub(r'\$LEVEL', lc, self._style._fmt) + RESET
        return Formatter.format(self, record)

    def _color_brackets(self, brackets_color):
        reg = '|'.join([re.escape(v) for _, v in _WORD_TO_COLOR.items()]
                       + [fr'\$LEVEL|{re.escape(BOLD)}|{re.escape(RESET)}|$'])
        segments = re.findall(f'((({reg})+)(.+?))(?={reg})', self._style._fmt)
        color_segment = [(c[1], c[3]) for c in segments]
        self._style._fmt = ''.join(
            re.sub(r'([\[\]])', fr'{brackets_color}\1{color}', part)
            for color, part in color_segment
        )


def _init_record(record: LogRecord) -> None:
    """Make certain a LogRecord will be using its original values.

    First time called will add original values to a LogRecord as new
    parameters. Subsequent calls will reset a LogRecords parameters back
    to the originals.

    This is so that other handlers won't have the colors inserted from
    previous ones.

    :param record: LogRecord to load with initial values.
    """
    record.msg = str(record.msg)
    try:
        if record.consumed:
            record.msg = record.original_msg
            record.args = record.original_args
    except AttributeError:
        record.original_msg = record.msg
        record.original_args = record.args
        record.consumed = True


def _format_message(msg: str, use_color: bool, bold: str) -> str:
    """Apply colors and styles where designated.

    :param msg: msg to format.
    :param use_color: Color words in msg will be replaced by colors if
        True else they will be replaced with empty strings.
    :param bold: Bold sequence or empty string.
    :return: The processed msg.
    """
    if not use_color:
        return re.sub(r'\$[A-Z_]+\b', '', msg)
    msg = f'{bold}{msg}$RESET'
    msg = re.sub(r'\$(RESET|R(?!ED))', RESET + bold, msg)
    msg = re.sub(r'\$(BOLD|B(?!LUE|LACK))', BOLD, msg)
    for color_word, color in _WORD_TO_COLOR.items():
        msg = msg.replace(f'${color_word}', color + bold)
    return msg
