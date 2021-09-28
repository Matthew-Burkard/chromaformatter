import logging
import sys

from chromaformatter import ChromaFormatter, Colors


def main() -> None:
    log_format = (
        f"{Colors.Style.BRIGHT}{Colors.Fore.GREEN}%(asctime)-s "
        f"{Colors.Style.BRIGHT}{Colors.LEVEL_COLOR}%(levelname).1s "
        f"{Colors.Style.BRIGHT}{Colors.Fore.MAGENTA}%(filename)-s:%(lineno)03d "
        f"{Colors.Style.BRIGHT}{Colors.LEVEL_COLOR}- %(message)s"
    )
    formatter = ChromaFormatter(
        log_format,
        f"{Colors.Style.BRIGHT}{Colors.Fore.WHITE}",
        f"{Colors.Style.BRIGHT}{Colors.LEVEL_COLOR}",
    )
    log_demo("colored", formatter)
    log_format = "%(asctime)-s %(levelname).1s %(filename)-s:%(lineno)03d - %(message)s"
    formatter = ChromaFormatter(log_format)
    print()
    log_demo("uncolored", formatter)


def log_demo(name: str, formatter: ChromaFormatter) -> None:
    log = logging.getLogger(name)
    while log.handlers:
        log.removeHandler(log.handlers.pop())
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    log.setLevel(logging.DEBUG)

    log.debug("Something %s.", "technical")
    log.info("Something %s.", "normal")
    log.warning("Something looks %s.", "wrong")
    log.error("Something is %s.", "wrong")
    log.critical("Something is %s.", "very wrong")


if __name__ == "__main__":
    main()
