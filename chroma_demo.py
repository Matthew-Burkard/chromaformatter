import sys

from src import chromalogging as logging

if __name__ == '__main__':
    log = logging.getLogger()
    log_format = ('[$GREEN%(asctime)-s$R][%(levelname)-7s$R][$MAGENTA'
                  '%(filename)-s$R:$MAGENTA%(lineno)-d$R]: %(message)s')
    file_formatter = logging.ChromaFormatter(log_format, False, False)
    file_handler = logging.FileHandler('log/demo.log', mode='w')
    file_handler.setFormatter(file_formatter)
    stream_formatter = logging.ChromaFormatter(log_format, True, True)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(stream_formatter)
    log.addHandler(stream_handler)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)

    log.debug('This is a {} message.', 'debug')
    log.info('This is an {} message.', 'info')
    log.warning('This is a {} message.', 'warning')
    log.error('This is an {} message.', 'error')
    log.critical('This is a {} message.', 'critical')
    log.info('Inserted {} get {} formatting.', 'arguments', 'special')
    log.info(f'Info message with {"regular"} %s args.', 'formatting')

    logging.color_map[logging.INFO] = logging.Fore.WHITE
    logging.color_map[logging.BRACKET] = logging.Fore.RED
    logging.color_map[logging.ARGS] = logging.Fore.MAGENTA
    log.info('Altered colors {} message.', 'info')
