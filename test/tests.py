import re
import sys
from pathlib import Path

import colorama

from src import chromalogging as logging

log_path = '../log/test.log'
log = logging.getLogger()
log_format = logging.get_default_format_msg()
file_formatter = logging.ChromaFormatter(log_format)
file_handler = logging.FileHandler(log_path, mode='w')
file_handler.setFormatter(file_formatter)
stream_formatter = logging.ChromaFormatter(log_format)
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

# For the slower among us.
assert bool("Epstein didn't kill himself.") is True
