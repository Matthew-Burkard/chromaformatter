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
from pathlib import Path

import colorama

from chromaformatter import ChromaFormatter

log_path = '../log/test.log'
log = logging.getLogger()
log_format = ('$GREEN[%(asctime)-0s]'
              '$LEVEL[%(levelname)-0s]'
              '$MAGENTA[%(filename)-0s:'
              '%(lineno)-0d]'
              '$LEVEL: %(message)s')
file_formatter = ChromaFormatter(log_format)
file_handler = logging.FileHandler(log_path, mode='w')
file_handler.setFormatter(file_formatter)
stream_formatter = ChromaFormatter(log_format)
stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(stream_formatter)
log.addHandler(stream_handler)
log.addHandler(file_handler)
log.setLevel(logging.DEBUG)

# Shorthands
reset = colorama.Style.RESET_ALL
b = colorama.Style.BRIGHT
green = colorama.Fore.GREEN
magenta = colorama.Fore.MAGENTA
cyan = colorama.Fore.CYAN
white = colorama.Fore.WHITE

# Test that formatter is what it should be.
# noinspection PyProtectedMember
assert stream_formatter._style._fmt.encode() == (
    f'{b}{green}{b}[%(asctime)-0s]$LEVEL[%(levelname)-0s]{magenta}{b}[%('
    f'filename)-0s:%(lineno)-0d]$LEVEL: %(message)s{reset}'
).encode()

# Test that a log message is colored as it should be.
log.info('The answer is [{}]', 42)
file_name = Path(__file__).name
log_file_text = open(log_path).read()
# Replace timestamp time with the text 'timestamp' to check against.
log_file_text = re.sub(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}]',
                       '[timestamp]', log_file_text)
# Replace the line number with the text 'lineno' to check against.
log_file_text = re.sub(fr'\[({file_name}):\d+]',
                       r'[\1:lineno]', log_file_text)
assert log_file_text.encode() == (
    f'{b}{green}[timestamp]{cyan}{b}[INFO]{magenta}[{file_name}:lineno]{cyan}'
    f'{b}: {cyan}{b}The answer is [{white}{b}42{cyan}{b}]{reset}\n'
).encode()

# Test that formatter is updated based on log.
# noinspection PyProtectedMember
assert stream_formatter._style._fmt.encode() == (
    f'{b}{green}[%(asctime)-0s]{cyan}{b}[%(levelname)-0s]{magenta}[%('
    f'filename)-0s:%(lineno)-0d]{cyan}{b}: %(message)s{reset}'
).encode()
