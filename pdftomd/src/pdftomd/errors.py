"""Structured messages translated by the GUI at display time."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Notice:
    key: str
    detail: str = ""


class ConversionError(Exception):
    def __init__(self, key: str, detail: str = "") -> None:
        self.notice = Notice(key, detail)
        super().__init__(f"{key}: {detail}")


class Cancelled(Exception):
    """The user requested cancellation before an output was published."""
