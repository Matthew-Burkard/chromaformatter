import sys
from logging import *
from typing import Optional, Any

from colorama import init

from chromalogging.chroma_formatter import (ARGS, BRACKETS, RESET, BOLD,
                                            ChromaFormatter)

__all__ = ['ARGS', 'BRACKETS', 'RESET', 'BOLD', 'ChromaFormatter',
           'default_format_msg', 'get_default_logger'] + \
          ['BASIC_FORMAT', 'BufferingFormatter', 'CRITICAL', 'DEBUG', 'ERROR',
           'FATAL', 'FileHandler', 'Filter', 'Formatter', 'Handler', 'INFO',
           'LogRecord', 'Logger', 'LoggerAdapter', 'NOTSET', 'NullHandler',
           'StreamHandler', 'WARN', 'WARNING', 'addLevelName', 'basicConfig',
           'captureWarnings', 'critical', 'debug', 'disable', 'error',
           'exception', 'fatal', 'getLevelName', 'getLogger', 'getLoggerClass',
           'info', 'log', 'makeLogRecord', 'setLoggerClass', 'shutdown',
           'warn', 'warning', 'getLogRecordFactory', 'setLogRecordFactory',
           'lastResort', 'raiseExceptions']

init()


def default_format_msg(levelname_min: int = 0,
                       filename_min: int = 0,
                       lineno_min: int = 0,
                       asctime_min: int = 0,
                       ts_color: str = '$GREEN',
                       file_color: str = '$MAGENTA') -> str:
    """Get a pre-configured format string for ChromaFormatter.

    :param levelname_min: Minimum length for levelname, default 0.
    :param filename_min: Minimum length for filename_len, default 0.
    :param lineno_min: Minimum length for lineno_len, default 0.
    :param asctime_min: Minimum length for asctime_len, default 0.
    :param file_color: File color in the log msg, defaults to MAGENTA.
    :param ts_color: Timestamp color in the log msg, defaults to GREEN.
    :return: A format string.
    """
    return (f'{ts_color}[%(asctime){asctime_min}-s]'
            f'$LEVEL[%(levelname)-{levelname_min}s]'
            f'{file_color}[%(filename){filename_min}-s:'
            f'%(lineno)-{lineno_min}d]'
            f'$LEVEL: %(message)s')


def get_default_logger(level: Optional[int] = None,
                       name: Optional[str] = None,
                       filepath: Optional[str] = None,
                       format_string: Optional[str] = None,
                       **format_kwargs: Any) -> Logger:
    """Get a logger with default level, formatter, and handlers.

    :param level: Logging level, defaults to DEBUG.
    :param name: Optional logger name, default None.
    :param filepath: Optional string if provided will create a file
        handler using filepath.
    :param format_string: Log format to pass to ChromaFormatter,
        defaults to null. format_kwargs will be ignored if this is
        provided.
    :param format_kwargs: kwargs will be passed to default_format_msg.
    :return: A logger with default formatting and a default stream
        handler using stdout.
    """
    logger = getLogger(name)
    log_format = default_format_msg(**format_kwargs)
    formatter = ChromaFormatter(format_string or log_format)
    stream_handler = StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    if filepath:
        file_handler = FileHandler(filepath)
        file_formatter = ChromaFormatter(log_format, False, False)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    logger.setLevel(level or DEBUG)
    return logger
