import re
import sys
from logging import *

from colorama import init, Fore, Style

init()

ARGS = -10
BRACKETS = -20

RESET = Style.RESET_ALL
BOLD = Style.BRIGHT

_COLOR_INPUT = '{}'
_WORD_TO_COLOR = {
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


def default_format_msg(levelname_min=0, filename_min=0,
                       lineno_min=0, asctime_min=0,
                       ts_color='$GREEN', file_color='$MAGENTA'):
    """Get a pre-configured format string for ChromaFormatter.

    :param levelname_min: Minimum length for levelname, default 0.
    :type levelname_min: int

    :param filename_min: Minimum length for filename_len, default 0.
    :type filename_min: int

    :param lineno_min: Minimum length for lineno_len, default 0.
    :type lineno_min: int

    :param asctime_min: Minimum length for asctime_len, default 0.
    :type asctime_min: int

    :param file_color: Color of the file in the log msg,
        defaults to MAGENTA.
    :type file_color: str

    :param ts_color: Color of the timestamp in the log msg,
        defaults to GREEN.
    :type ts_color: str

    :return: A format string.
    :rtype: str
    """
    return (f'{ts_color}[%(asctime){asctime_min}-s]'
            f'$LEVEL[%(levelname)-{levelname_min}s]'
            f'{file_color}[%(filename){filename_min}-s:'
            f'%(lineno)-{lineno_min}d]'
            f'$LEVEL: %(message)s')


def get_default_logger(level=None, name=None, filepath=None, **format_kwargs):
    """Get a logger with default level, formatter, and handlers.

    :param level: Logging level, defaults to DEBUG.
    :type level: int

    :param name: Optional logger name, default None.
    :type name: str

    :param filepath: Optional string if provided will create a file
        handler using filepath.
    :type filepath: str

    :param format_kwargs: kwargs will be passed to
        default_format_msg.
    :type format_kwargs: typing.Any

    :return: A logger with default formatting and a default stream
        handler using stdout.
    :rtype: Logger
    """
    logger = getLogger(name)
    log_format = default_format_msg(*format_kwargs)
    formatter = ChromaFormatter(log_format)
    stream_handler = StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    if filepath:
        file_handler = FileHandler(filepath)
        file_formatter = ChromaFormatter(log_format, False, False)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    logger.setLevel(level or DEBUG)
    return logger


# noinspection PyProtectedMember
class ChromaFormatter(Formatter):
    """Extends logging.Formatter to add colors and styles"""

    def __init__(self, msg, use_color=True, all_bold=True):
        """Create an instance of ChromaFormatter.

        :param msg: The format string to determine how logs will appear.
        :type msg: str

        :param use_color: Colors will be applied if True, defaults to
            True.
        :type use_color: bool

        :param all_bold: Whole log will be bold if True, defaults to
            True.
        :type all_bold: bool
        """
        self.use_color = use_color
        self.all_bold = BOLD if all_bold else ''
        msg = _format_message(msg, use_color, self.all_bold)
        super().__init__(msg)
        if use_color:
            self._original_style_fmt = self._style._fmt

        self.color_map = {
            DEBUG: Fore.BLUE,
            INFO: Fore.CYAN,
            WARNING: Fore.YELLOW,
            ERROR: Fore.LIGHTRED_EX,
            CRITICAL: Fore.RED,
            ARGS: Fore.WHITE,
            BRACKETS: ''
        }

    def format(self, record):
        _init_record(record)
        if not self.use_color or record.levelno not in self.color_map:
            record.msg = re.sub(r'(?<!{){}(?!})', '[%s]', record.msg)
        if not self.use_color or record.levelno not in self.color_map:
            return Formatter.format(self, record)
        self._style._fmt = self._original_style_fmt
        if self.all_bold:
            self._style._fmt = re.sub(re.escape(BOLD), '', self._style._fmt)
            self._style._fmt = BOLD + self._style._fmt
        # Shorthands for different colors.
        bc = self.color_map[BRACKETS] + self.all_bold
        ac = self.color_map[ARGS] + self.all_bold
        lc = self.color_map[record.levelno] + self.all_bold
        if self.color_map[BRACKETS]:
            self._color_brackets(bc)
        record.msg = lc + record.msg
        if record.args:
            record.msg = re.sub(r'(?<!{){}(?!})',
                                f'{ac}{bc}[{ac}%s{bc}]{lc}', record.msg)
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


def _init_record(record):
    """Make certain a LogRecord will be using it's original values.

    First time called will add original values to a LogRecord, as new
    parameters. Subsequent calls will reset a LogRecords parameters back
    to the originals.

    This is so that other handlers won't have the colors inserted from
    previous ones.

    :param record: LogRecord to load with initial values.
    :type record: LogRecord
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


def _format_message(msg, use_color, all_bold):
    """Apply colors and styles where designated.

    :param msg: msg to format.
    :type msg: str

    :param use_color: Color words in msg will be replaced by colors if
        True else they will be replaced with empty strings.
    :type use_color: bool

    :param all_bold: Bold sequence or empty string.
    :type all_bold: str

    :return: The processed msg.
    :rtype: str
    """
    if not use_color:
        return re.sub(r'\$[A-Z_]+\b', '', msg)
    msg = f'{all_bold}{msg}$RESET'
    msg = re.sub(r'\$(RESET|R(?!ED))', RESET + all_bold, msg)
    msg = re.sub(r'\$(BOLD|B(?!LUE|LACK))', BOLD, msg)
    for color_word, color in _WORD_TO_COLOR.items():
        msg = msg.replace(f'${color_word}', color + all_bold)
    return msg
