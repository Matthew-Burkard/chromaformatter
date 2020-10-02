import sys

from src import chromalogging as logging


def log_as(log_format, all_bold, msg, *args) -> None:
    log = logging.getLogger()
    stream_formatter = logging.ChromaFormatter(log_format, all_bold=all_bold)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(stream_formatter)
    log.addHandler(stream_handler)
    log.setLevel(logging.DEBUG)
    log.debug(msg, *args)
    log.info(msg, *args)
    log.warning(msg, *args)
    log.error(msg, *args)
    log.critical(msg, *args)
    log.removeHandler(stream_handler)
    print()


if __name__ == '__main__':
    test_format = ('$GREEN[%(asctime)-s]'
                   '$LEVEL[%(levelname)-8s]'
                   '$MAGENTA[%(filename)-s:'
                   '%(lineno)-d]$LEVEL: %(message)s')
    default = logging.get_default_format_msg(8, 9, 3, 24)

    log_as(default, False, 'Test message {} should not be bold.', 'one')
    log_as(default, True, 'Test message {} should be bold.', 'two')
    log_as(default, False, 'Test message {} should not be bold.', 'three')
    log_as(test_format, False, 'Test message {} should have bold ts.', 'four')
    log_as(test_format, True,
           'Test message {} should be bold with no errors from repeat bolds.',
           'five')
    log_as(test_format, True,
           'Test message {} colors should be identical to test two.',
           'six')
