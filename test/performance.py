import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

from chromaformatter import Colors, ChromaFormatter

num_iterations = 10001


def test(current_formatter: logging.Formatter, name: str) -> timedelta:
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(current_formatter)
    log = logging.getLogger(name)
    log_dir = Path(__file__).parent / "log" / "performance.log"
    file_handler = logging.FileHandler(log_dir, mode="w")
    log.addHandler(handler)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)
    start = datetime.now()
    for i in range(1, num_iterations):
        log.info(f"info {i}")
        log.debug(f"debug {i}")
        log.warning(f"warning {i}")
        log.error(f"error {i}")
        log.critical(f"critical {i}")
    return datetime.now() - start


format_string = "%(asctime)-s %(levelname)-8s %(filename)-s:%(lineno)-0d: %(message)s"
formatter = logging.Formatter(format_string)
chroma_format_string = (
    f"{Colors.Fore.GREEN}%(asctime)-s"
    f" {Colors.LEVEL_COLOR}%(levelname)-8s"
    f" {Colors.Fore.MAGENTA}%(filename)-s:%(lineno)-0d"
    f"{Colors.LEVEL_COLOR}: %(message)s"
)
chroma_formatter = ChromaFormatter(chroma_format_string)

normal_time = test(formatter, "normal")
chroma_time = test(chroma_formatter, "colored")

print(f"{num_iterations - 1} normal logs in [{normal_time}]")
print(f"{num_iterations - 1} chroma logs in [{chroma_time}]")
