import sys

import colorama

from src import chromalogging as logging

if __name__ == '__main__':
    log = logging.getLogger()
    log_format = logging.default_format_msg(levelname_min=5)
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
    log.info('Inserted {} get {} formatting.', 'arguments', 'special')
    reg = 'regular'
    formatting = 'formatting'
    log.info(f'Info message with {reg} {formatting}.')

    stream_formatter.color_map[logging.INFO] = colorama.Fore.WHITE
    stream_formatter.color_map[logging.BRACKETS] = colorama.Fore.RESET
    stream_formatter.color_map[logging.ARGS] = colorama.Fore.CYAN
    log.info('Altered colors {} message.', 'info')

    format_string = (f'$GREEN%(asctime)-s'
                     f' $LEVEL%(levelname)-s'
                     f' $MAGENTA%(filename)-s:%(lineno)-0d'
                     f'$LEVEL: %(message)s')
    formatter = logging.ChromaFormatter(format_string)
    formatter.add_brackets_to_args = False
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    log.removeHandler(stream_handler)
    log.addHandler(handler)
    log.info('New {} log format.', 'ChromaFormatter')
