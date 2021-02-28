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
import logging
import re
import sys
import unittest
from pathlib import Path

import colorama

from chromaformatter import ChromaFormatter

# Shorthands
reset = colorama.Style.RESET_ALL
b = colorama.Style.BRIGHT
green = colorama.Fore.GREEN
magenta = colorama.Fore.MAGENTA
cyan = colorama.Fore.CYAN
white = colorama.Fore.WHITE


class UtilTest(unittest.TestCase):

    def __init__(self, *args) -> None:
        self.log_path = 'log/test.log'
        self.log = logging.getLogger()
        log_format = ('$GREEN[%(asctime)-0s]'
                      '$LEVEL[%(levelname)-0s]'
                      '$MAGENTA[%(filename)-0s:'
                      '%(lineno)-0d]'
                      '$LEVEL: %(message)s')
        file_formatter = ChromaFormatter(log_format)
        file_handler = logging.FileHandler(self.log_path, mode='w')
        file_handler.setFormatter(file_formatter)
        self.stream_formatter = ChromaFormatter(log_format)
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(self.stream_formatter)
        self.log.addHandler(stream_handler)
        self.log.addHandler(file_handler)
        self.log.setLevel(logging.DEBUG)
        super(UtilTest, self).__init__(*args)

    def test_formatter_style(self) -> None:
        # noinspection PyProtectedMember
        self.assertEqual(
            self.stream_formatter._style._fmt.encode(),
            f'{green}[%(asctime)-0s]$LEVEL'
            f'[%(levelname)-0s]{magenta}[%(filename)-0s:%(lineno)-0d]'
            f'$LEVEL: %(message)s{reset}'.encode()
        )

    def test_log_color(self) -> None:
        # Test that a log message is colored as it should be.
        self.log.info('The answer is [%s]', 42)
        file_name = Path(__file__).name
        with open(self.log_path) as f:
            log_file_text = f.read()
            # Replace timestamp time with the text 'timestamp' to check
            # against.
            log_file_text = re.sub(
                r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}]',
                '[timestamp]',
                log_file_text
            )
            # Replace the line number with the text 'lineno' to check
            # against.
            log_file_text = re.sub(fr'\[({file_name}):\d+]',
                                   r'[\1:lineno]', log_file_text)
            self.assertEqual(
                log_file_text.encode(),
                f'{green}[timestamp]{cyan}[INFO]{magenta}'
                f'[{file_name}:lineno]{cyan}'
                f': {cyan}The answer is'
                f' [{white}42{cyan}]{reset}\n'.encode()
            )

    def test_something(self) -> None:
        # Test that formatter is updated based on log.
        # noinspection PyProtectedMember
        self.assertEqual(
            self.stream_formatter._style._fmt.encode(),
            f'{green}[%(asctime)-0s]{cyan}[%(levelname)-0s]{magenta}[%('
            f'filename)-0s:%(lineno)-0d]{cyan}: %(message)s{reset}'.encode()
        )


if __name__ == '__main__':
    unittest.main()
