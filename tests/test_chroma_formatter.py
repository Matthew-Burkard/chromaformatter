"""Chroma Formatter unit tests."""
import logging
import os
import re
import sys
import unittest
import uuid
from pathlib import Path

from chromaformatter import ChromaFormatter, Colors


class UtilTest(unittest.TestCase):
    def __init__(self, *args) -> None:
        self.log_path = f"{os.getcwd()}/log"
        Path(self.log_path).mkdir(exist_ok=True)
        self.log = logging.getLogger(__name__)
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
        file_handler = logging.FileHandler(f"{self.log_path}/test.log", mode="w")
        file_handler.setFormatter(self.formatter)
        self.stream_handler = logging.StreamHandler(stream=sys.stdout)
        self.stream_handler.setFormatter(self.formatter)
        self.log.addHandler(self.stream_handler)
        self.log.addHandler(file_handler)
        self.log.setLevel(logging.DEBUG)
        super(UtilTest, self).__init__(*args)

    def test_custom_level(self) -> None:
        log = logging.getLogger(str(uuid.uuid4()))
        log.addHandler(self.stream_handler)
        log.log(
            100,
            "It was not until [%s] that light was identified as the source of"
            " the color sensation.",
            "Newton",
        )

    def test_log_color(self) -> None:
        # Test that a log message is colored as it should be.
        log_filepath = f"{self.log_path}/test.log"
        self.log.info(
            "It was not until [%s] that light was identified as the source of"
            " the color sensation.",
            "Newton",
        )
        file_name = Path(__file__).name
        log_file_text = Path(log_filepath).read_text()
        # Replace timestamp time with the text 'timestamp' to check
        # against.
        log_file_text = re.sub(
            r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}]",
            "[timestamp]",
            log_file_text,
        )
        # Replace the line number with the text 'lineno' to check
        # against.
        log_file_text = re.sub(rf"\[({file_name}):\d+]", r"[\1:lineno]", log_file_text)
        self.assertEqual(
            f"{Colors.Fore.GREEN}[timestamp]{Colors.Fore.CYAN}[INFO]"
            f"{Colors.Fore.MAGENTA}[{file_name}:lineno]"
            f"{Colors.Fore.CYAN}: It was not until"
            f" [{Colors.Fore.WHITE}Newton{Colors.Fore.CYAN}]"
            f" that light was identified as the source"
            f" of the color sensation.{Colors.Style.RESET_ALL}\n".encode(),
            log_file_text.encode(),
        )

    def test_format(self) -> None:
        # Test that formatter is updated based on log.
        # noinspection PyProtectedMember
        self.assertEqual(
            f"{Colors.Fore.GREEN}[%(asctime)-0s]"
            f"{Colors.Fore.LIGHTBLUE_EX}[%(levelname)-0s]"
            f"{Colors.Fore.MAGENTA}[%(filename)-0s:%(lineno)-0d]"
            f"{Colors.Fore.LIGHTBLUE_EX}: %(message)s"
            f"{Colors.Style.RESET_ALL}",
            self.formatter._style._fmt.replace("$LEVEL", Colors.Fore.LIGHTBLUE_EX),
        )
