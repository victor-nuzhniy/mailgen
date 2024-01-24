"""Services for mailgen app."""
from __future__ import annotations

import ctypes
import re
from typing import Any, Callable

from mailgen.common.constants import VERIFIED_EMAIL_DOMAINS
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


class Searchers(object):
    """Searchers for different cases."""

    def check_email_is_verified(self, email: str) -> str:
        """
        Check whether email with domain in verified emails domains list.

        :param email: str Email for verification.

        :return: str Email or empty string in case not belonging.
        """
        for domain in VERIFIED_EMAIL_DOMAINS:
            if email.endswith(domain):
                return email
        return ''

    def search_email(self, text: str) -> str:
        """
        Search first email in text.

        :param text: str Text to search regex in.

        :return: str Found email or empty string.
        """
        match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
        if match:
            email: str = str(match.group(0))
            return self.check_email_is_verified(email)
        return ''

    def search_six_digits(self, text: str) -> str:
        """
        Search first six digits in text.

        :param text: str Text to search regex in.

        :return: str Found six-digits string or empty string.
        """
        match = re.search(r'(\d{6})', text)
        if match:
            return str(match.group(0))
        return ''

    def search_captcha_word(self, text: str) -> str:
        """
        Search 'CAPTCHA' and '... unavailable'.

        :param text:
        :return:
        """
        match = re.search('CAPTCHA', text)
        second_match = re.search('CAPTCHA verification is currently unavailable', text)
        if match and not second_match:
            return 'CAPTCHA'
        return ''

    def search_email_word(self, text: str) -> str:
        """
        Search 'Email' word in text.

        :param text: str Text from the clipboard.
        :return: str 'email' word or empty string.
        """
        match = re.search('Email', text)
        if match:
            return 'Email'
        return ''

    def search_email_verif_phrase(self, text: str) -> str:
        """
        Search 'Get verification code' phrase.

        :param text: str Text from the clipboard.
        :return: str 'Found' word or empty string.
        """
        match = re.search('Get verification code', text)
        if match:
            return 'Found'
        return ''


class AppSearchers(Searchers):
    """App searchers for different cases."""


app_searchers = AppSearchers()
