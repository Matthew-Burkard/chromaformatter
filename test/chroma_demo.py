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

import sys
import logging

import colorama

import chromaformatter
from chromaformatter import ChromaFormatter


def main(use_color: bool) -> None:
    log = logging.getLogger()
    while log.handlers:
        log.removeHandler(log.handlers.pop())
    log_format = ('$GREEN[%(asctime)-s]'
                  '$LEVEL[%(levelname)-8s]'
                  '$MAGENTA[%(filename)-s:%(lineno)-d]'
                  '$LEVEL: %(message)s')
    file_formatter = ChromaFormatter(log_format, False)
    file_handler = logging.FileHandler('./log/demo.log', mode='w')
    file_handler.setFormatter(file_formatter)
    stream_formatter = ChromaFormatter(log_format, use_color, use_color)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(stream_formatter)
    log.addHandler(stream_handler)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)

    log.debug('This is a debug message.')
    log.info('This is an info message.', )
    log.warning('This is a warning message.')
    log.error('This is an error message.')
    log.critical('This is a critical message.')
    log.info('Formatted {} can get {} coloring.', 'arguments', 'custom')

    stream_formatter.color_map[logging.INFO] = colorama.Fore.WHITE
    stream_formatter.color_map[chromaformatter.ARGS] = colorama.Fore.CYAN
    log.info('Altered colors {} message.', 'info')

    format_string = ('$LEVEL%(levelname)-s'
                     ' $GREEN%(asctime)-s'
                     ' $MAGENTA%(filename)-s:%(lineno)-0d'
                     '$LEVEL: %(message)s')
    formatter = ChromaFormatter(format_string, use_color, use_color)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    log.removeHandler(stream_handler)
    log.addHandler(handler)
    log.info('New {} log format.', 'ChromaFormatter')


if __name__ == '__main__':
    main(True)
    print()
    main(False)
