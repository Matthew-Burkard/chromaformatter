import sys

import colorama

from src import chromalogging as logging

if __name__ == '__main__':
    log = logging.getLogger()
    log_format = logging.default_format_msg(levelname_min=8)
    file_formatter = logging.ChromaFormatter(log_format, False, False)
    file_handler = logging.FileHandler('log/demo.log', mode='w')
    file_handler.setFormatter(file_formatter)
    stream_formatter = logging.ChromaFormatter(log_format)
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
    log.info('Formatted {} get {} coloring.', 'arguments', 'special')

    stream_formatter.color_map[logging.INFO] = colorama.Fore.WHITE
    stream_formatter.color_map[logging.ARGS] = colorama.Fore.CYAN
    log.info('Altered colors {} message.', 'info')

    format_string = ('$LEVEL%(levelname)-s'
                     ' $GREEN%(asctime)-s'
                     ' $MAGENTA%(filename)-s:%(lineno)-0d'
                     '$LEVEL: %(message)s')
    formatter = logging.ChromaFormatter(format_string)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    log.removeHandler(stream_handler)
    log.addHandler(handler)
    log.info('New {} log format.', 'ChromaFormatter')
