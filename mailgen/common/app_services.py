"""Services for mailgen app."""
from __future__ import annotations

import ctypes
import re
from typing import Any, Callable

from mailgen.common.exceptions import ClipboardRetrieveDataError


class WindllService(object):
    """Storage with methods to perform CRUD operations, Singlton."""

    _kernel32 = ctypes.windll.kernel32
    _user32 = ctypes.windll.user32
    _cf_text = 1

    def __new__(cls, *args: Any, **kwargs: Any) -> WindllService:
        """Create new instance, if it's None, otherwise use earlier created one."""
        if getattr(cls, 'instance', None) is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self) -> None:
        """Initialize WindllService instance."""
        self._kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
        self._kernel32.GlobalLock.restype = ctypes.c_void_p
        self._kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
        self._user32.GetClipboardData.restype = ctypes.c_void_p

    def get_clipboard_data(self, operator: Callable) -> str:
        """
        Get data from clipboard using operator function.

        :param operator: Callable Operator to perform search with.

        :return: str Found element or empty string.
        """
        self._user32.OpenClipboard(0)
        try:
            return self._search_elements(operator)
        except ClipboardRetrieveDataError:  # add logging info
            return ''
        finally:
            self._user32.CloseClipboard()

    def _search_elements(self, operator: Callable) -> str:
        """
        Get data from clipboard using operator function.

        :param operator: Callable Operator to perform search with.

        :return: str Found element or empty string.
        """
        if self._user32.IsClipboardFormatAvailable(self._cf_text):
            clipboard_data = self._user32.GetClipboardData(self._cf_text)
            data_locked = self._kernel32.GlobalLock(clipboard_data)
            text = ctypes.c_char_p(data_locked)
            return operator(str(text.value))
        return ''


def search_email(text: str) -> str:
    """
    Search first email in text.

    :param text: str Text to search regex in.

    :return: str Found email or empty stging.
    """
    if '@dropmail.me' in text or '@10mail.org' in text or '@emltmp.com' in text:
        match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
        if match:
            return str(match.group(0))
    return ''


def search_six_digits(text: str) -> str:
    """
    Search first six digits in text.

    :param text: str Text to search regex in.

    :return: str Found six-digits string or '111111'.
    """
    match = re.search(r'(\d{6})', text)
    if match:
        return str(match.group(0))
    return '111111'
