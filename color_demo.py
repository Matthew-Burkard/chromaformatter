import sys

from src import chromalogging as logging

if __name__ == '__main__':
    log = logging.getLogger("NAME")
    log_format = '$RESET$BOLD[$RESET$GREEN%(asctime)s$RESET$BOLD][$RESET' \
                 '%(levelname)-6s$BOLD]:$RESET %(message)s $RESET$BOLD[$RESET' \
                 '$MAGENTA$BOLD%(filename)s:$RESET%(lineno)-d$BOLD]$RESET'
    colored_formatter = logging.ColoredFormatter(log_format, True)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(colored_formatter)
    log.addHandler(stream_handler)
    log.setLevel(logging.DEBUG)

    log.debug('This is a {} message.', 'debug')
    log.info('This is an {} message.', 'info')
    log.warning('This is a {} message.', 'warning')
    log.error('This is an {} message.', 'error')
    log.critical('This is a {} message.', 'critical')

    logging.COLOR_MAP[logging.INFO] = logging.Colors.CYAN
    logging.COLOR_MAP[logging.BRACKET] = logging.Colors.RED
    logging.COLOR_MAP[logging.ARGS] = logging.Colors.MAGENTA
    log.info('Altered colors {} message.', 'info')

    logging.COLOR_MAP[logging.INFO] = logging.Colors.WHITE
    log.info('Solid color [%s] message.', 'info')
