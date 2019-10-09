import sys

from src import chromalogging as logging

if __name__ == '__main__':
    log = logging.getLogger()
    log_format = '[$GREEN%(asctime)s$R][%(levelname)-6s$R]: %(message)s ' \
                 '$R[$MAGENTA%(filename)s$R:$MAGENTA%(lineno)-d$R]'
    file_formatter = logging.ChromaFormatter(log_format, False, True)
    file_handler = logging.FileHandler('log/demo.log', mode='w')
    file_handler.setFormatter(file_formatter)
    stream_formatter = logging.ChromaFormatter(log_format, True, True)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(stream_formatter)
    log.addHandler(stream_handler)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)

    log.info('Inserted {} get {} formatting.', 'arguments', 'special')
    log.debug('This is a {} message.', 'debug')
    log.info('This is a {} message.', 'info')
    log.warning('This is a {} message.', 'warning')
    log.error('This is an {} message.', 'error')
    log.critical('This is a {} message.', 'critical')
    log.info(f'Debug message with {"regular"} %s args.', 'formatting')

    logging.color_map[logging.INFO] = logging.Colors.CYAN
    logging.color_map[logging.BRACKET] = logging.Colors.RED
    logging.color_map[logging.ARGS] = logging.Colors.MAGENTA
    log.info('Altered colors {} message.', 'info')

    logging.color_map[logging.INFO] = logging.Colors.WHITE
    logging.color_map[logging.BRACKET] = logging.Colors.WHITE
    logging.color_map[logging.ARGS] = logging.Colors.WHITE
    log.info('Solid color {} message.', 'info')