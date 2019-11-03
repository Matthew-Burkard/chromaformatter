import sys

from src import chromalogging as logging

if __name__ == '__main__':
    log = logging.getLogger()
    log_format = logging.default_format_msg(levelname_min=5)
    file_formatter = logging.ChromaFormatter(log_format, False, False)
    file_handler = logging.FileHandler('log/demo.log', mode='w')
    file_handler.setFormatter(file_formatter)
    stream_formatter = logging.ChromaFormatter(log_format, True, True)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(stream_formatter)
    log.addHandler(stream_handler)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)

    log.debug('This is a debug message.')
    log.info('This is an info message.',)
    log.warning('This is a warning message.')
    log.error('This is an error message.')
    log.critical('This is a critical message.')
    log.info('Inserted {} get {} formatting.', 'arguments', 'special')
    log.info(f'Info message with {"regular"} %s.', 'formatting')

    logging.color_map[logging.INFO] = logging.Fore.WHITE
    logging.color_map[logging.BRACKETS] = logging.Fore.RED
    logging.color_map[logging.ARGS] = logging.Fore.MAGENTA
    log.info('Altered colors {} message.', 'info')
