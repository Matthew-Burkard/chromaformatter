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
from logging import (Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL,
                     LogRecord, NOTSET)
from typing import Dict, Optional

import colorama

__all__ = (
    'ChromaFormatter',
    'Colors',
)


class Colors:
    Fore = colorama.Fore
    Back = colorama.Back
    Style = colorama.Style
    LEVEL_COLOR = '$LEVEL'


# noinspection PyProtectedMember
class ChromaFormatter(Formatter):
    """Extended logging.Formatter to add colors and styles."""

    def __init__(
            self,
            fmt: str,
            arg_start_color: Optional[str] = None,
            arg_end_color: Optional[str] = None
    ) -> None:
        """Set ChromaFormatter properties.

        :param fmt: The format string to determine how logs will appear.
        :param arg_start_color: Color of formatted arguments.
        :param arg_end_color: Color after formatted arguments.
        """
        fmt = f'{fmt}{Colors.Style.RESET_ALL}'
        super().__init__(fmt)
        self._original_style_fmt = self._style._fmt
        self.arg_start_color = arg_start_color
        self.arg_end_color = arg_end_color

        self.color_map: Dict[int, str] = {
            NOTSET: Colors.Fore.LIGHTBLUE_EX,
            DEBUG: Colors.Fore.BLUE,
            INFO: Colors.Fore.CYAN,
            WARNING: Colors.Fore.YELLOW,
            ERROR: Colors.Fore.LIGHTRED_EX,
            CRITICAL: Colors.Fore.RED
        }

    def format(self, record: LogRecord) -> str:
        """Format and add colors to a log record.

        :param record: LogRecord to format and color.
        :return: The complete log record formatted and colored.
        """
        msg = str(record.msg)
        if record.levelno not in self.color_map:
            return super(ChromaFormatter, self).format(record)
        self._style._fmt = self._original_style_fmt
        level_color = self.color_map[record.levelno]
        # Color the record msg.
        if record.args and self.arg_start_color and self.arg_end_color:
            record.msg = re.sub(
                r'(?<!%)%([-0.\d]*)([sd])',
                fr'{self.arg_start_color}%\1\2{self.arg_end_color}',
                record.msg
            ).replace('$LEVEL', level_color)
        self._style._fmt = self._style._fmt.replace(
            Colors.LEVEL_COLOR,
            level_color
        )
        s = super(ChromaFormatter, self).format(record)
        record.msg = msg
        return s
