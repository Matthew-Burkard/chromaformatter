import logging
import os
import sys
from datetime import datetime, timedelta

import chromaformatter


def test(current_formatter, name) -> timedelta:
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(current_formatter)
    log = logging.getLogger(name)
    log_dir = os.path.dirname(os.path.abspath(__file__)).replace('test', 'log')
    file_handler = logging.FileHandler(f'{log_dir}/performance.log', mode='w')
    log.addHandler(handler)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)
    start = datetime.now()
    for i in range(1, 10001):
        log.info(f'info {i}')
        log.debug(f'debug {i}')
        log.warning(f'warning {i}')
        log.error(f'error {i}')
        log.critical(f'critical {i}')
    return datetime.now() - start


format_string = ('%(asctime)-s'
                 ' %(levelname)-8s'
                 ' %(filename)-s:%(lineno)-0d: %(message)s')
formatter = logging.Formatter(format_string)
chroma_format_string = ('$GREEN%(asctime)-s'
                        ' $LEVEL%(levelname)-8s'
                        ' $MAGENTA%(filename)-s:%(lineno)-0d'
                        '$LEVEL: %(message)s')
chroma_formatter = chromaformatter.ChromaFormatter(chroma_format_string)

normal_time = test(formatter, 'normal')
chroma_time = test(chroma_formatter, 'colored')

print(f'50,000 normal logs in [{normal_time}]')
print(f'50,000 chroma logs in [{chroma_time}]')
