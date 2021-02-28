# Copyright © 2020 Matthew Burkard
#
# This file is part of Chroma Formatter.
#
# Chroma Formatter is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Chroma Formatter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Chroma Formatter.  If not, see <https://www.gnu.org/licenses/>.

import re
from logging import Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL, LogRecord
from typing import Dict, Any

from colorama import Fore, Style

__all__ = ('ChromaFormatter',)

ARGS = -10
_RESET = Style.RESET_ALL
_BOLD = Style.BRIGHT

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
    """Extended logging.Formatter to add colors and styles."""

    def __init__(self,
                 msg: str,
                 use_color: bool = True,
                 use_bold: bool = False) -> None:
        """Set ChromaFormatter properties.

        :param msg: The format string to determine how logs will appear.
        :param use_color: Colors will be applied if True, default True.
        :param use_bold: Whole log will be bold if True, default True.
        """
        self.use_color: bool = use_color
        self._bold: str = _BOLD if use_bold else ''
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
            ARGS: Fore.WHITE
        }

    def format(self, record: LogRecord) -> str:
        """Format and add colors to a log record.

        :param record: LogRecord to format and color.
        :return: The complete log record formatted and colored.
        """
        _init_record(record)
        if not self.use_color or record.levelno not in self.color_map:
            return Formatter.format(self, record)
        self._style._fmt = self._original_style_fmt
        if self._bold:
            self._style._fmt = re.sub(re.escape(_BOLD), '', self._style._fmt)
            self._style._fmt = _BOLD + self._style._fmt
        # Shorthands for different colors.
        arg_color = self.color_map[ARGS] + self._bold
        level_color = self.color_map[record.levelno] + self._bold
        # Color the record msg.
        record.msg = level_color + record.msg
        if record.args:
            record.msg = re.sub(r'(?<!%)%s',
                                f'{arg_color}%s{level_color}', record.msg)
        self._style._fmt = re.sub(r'\$LEVEL', level_color, self._style._fmt)
        return Formatter.format(self, record)


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
    msg = f'{bold}{msg}{_RESET}'
    msg = re.sub(r'\$RESET', _RESET + bold, msg)
    msg = re.sub(r'\$BOLD', _BOLD, msg)
    for color_word, color in _WORD_TO_COLOR.items():
        msg = msg.replace(f'${color_word}', color + bold)
    return msg
