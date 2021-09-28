import logging
import re
import sys
import unittest
from pathlib import Path

from chromaformatter import ChromaFormatter, Colors


class UtilTest(unittest.TestCase):
    def __init__(self, *args) -> None:
        self.log_path = "log/test.log"
        self.log = logging.getLogger()
        log_format = (
            f"{Colors.Fore.GREEN}[%(asctime)-0s]"
            f"{Colors.LEVEL_COLOR}[%(levelname)-0s]"
            f"{Colors.Fore.MAGENTA}[%(filename)-0s:"
            f"%(lineno)-0d]"
            f"{Colors.LEVEL_COLOR}: %(message)s"
        )
        self.formatter = ChromaFormatter(
            log_format, Colors.Fore.WHITE, Colors.LEVEL_COLOR
        )
        file_handler = logging.FileHandler(self.log_path, mode="w")
        file_handler.setFormatter(self.formatter)
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(self.formatter)
        self.log.addHandler(stream_handler)
        self.log.addHandler(file_handler)
        self.log.setLevel(logging.DEBUG)
        super(UtilTest, self).__init__(*args)

    def test_formatter_style(self) -> None:
        # noinspection PyProtectedMember
        self.assertEqual(
            self.formatter._style._fmt.encode(),
            f"{Colors.Fore.GREEN}[%(asctime)-0s]$LEVEL[%(levelname)-0s]"
            f"{Colors.Fore.MAGENTA}[%(filename)-0s:%(lineno)-0d]"
            f"{Colors.LEVEL_COLOR}: %(message)s"
            f"{Colors.Style.RESET_ALL}".encode(),
        )

    def test_log_color(self) -> None:
        # Test that a log message is colored as it should be.
        self.log.info(
            "It was not until [%s] that light was identified as the source of"
            " the color sensation.",
            "Newton",
        )
        file_name = Path(__file__).name
        with open(self.log_path) as f:
            log_file_text = f.read()
            # Replace timestamp time with the text 'timestamp' to check
            # against.
            log_file_text = re.sub(
                r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}]",
                "[timestamp]",
                log_file_text,
            )
            # Replace the line number with the text 'lineno' to check
            # against.
            log_file_text = re.sub(
                fr"\[({file_name}):\d+]", r"[\1:lineno]", log_file_text
            )
            self.assertEqual(
                log_file_text.encode(),
                f"{Colors.Fore.GREEN}[timestamp]{Colors.Fore.CYAN}[INFO]"
                f"{Colors.Fore.MAGENTA}[{file_name}:lineno]"
                f"{Colors.Fore.CYAN}: It was not until"
                f" [{Colors.Fore.WHITE}Newton{Colors.Fore.CYAN}]"
                f" that light was identified as the source"
                f" of the color sensation.{Colors.Style.RESET_ALL}\n".encode(),
            )

    def test_something(self) -> None:
        # Test that formatter is updated based on log.
        # noinspection PyProtectedMember
        self.assertEqual(
            self.formatter._style._fmt.encode(),
            f"{Colors.Fore.GREEN}[%(asctime)-0s]"
            f"{Colors.Fore.CYAN}[%(levelname)-0s]"
            f"{Colors.Fore.MAGENTA}[%(filename)-0s:%(lineno)-0d]"
            f"{Colors.Fore.CYAN}: %(message)s"
            f"{Colors.Style.RESET_ALL}".encode(),
        )


if __name__ == "__main__":
    unittest.main()
