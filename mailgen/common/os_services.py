"""Os specific services for mailgen app."""
from __future__ import annotations

import platform
from typing import Any
from winreg import HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, OpenKey, QueryValueEx

from mailgen.common.exceptions import ServiceUnavailableError


def get_registry_browser_info() -> str:
    """Get registry browser information."""
    with OpenKey(
        HKEY_CURRENT_USER,
        ''.join(
            (
                r'SOFTWARE\Microsoft\Windows\Shell\Associations',
                r'\UrlAssociations\http\UserChoice',
            ),
        ),
    ) as regkey:
        # Get the user choice
        browser_choice = QueryValueEx(regkey, 'ProgId')[0]
    with OpenKey(
        HKEY_CLASSES_ROOT,
        r'{key}\shell\open\command'.format(key=browser_choice),
    ) as regk:
        # Get the app the user's choice refers to in the application registrations
        browser_path_tuple = QueryValueEx(regk, '')

        # This is a bit sketchy and assumes that the path
        # will always be in double quotes
        browser_path = browser_path_tuple[0].split('"')[1]
    return browser_path.split('\\')[-1]


def get_default_browser() -> str:
    """Get default browser."""
    os_platform: str = platform.system()
    if os_platform == 'Windows':
        try:
            return get_registry_browser_info()
        except Exception as ex:
            raise ServiceUnavailableError(str(ex))
    raise ServiceUnavailableError('Mailgen is working on Windows only.')


class OsInfo(object):
    """Os information."""

    _default_browser: str = 'chrome.exe'
    _os_platform: str = 'Windows'

    def __new__(cls, *args: Any, **kwargs: Any) -> OsInfo:
        """Create new instance, if it's None, otherwise use earlier created one."""
        if getattr(cls, 'instance', None) is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self) -> None:
        """Initialize OsInfo instance."""
        self._default_browser = get_default_browser()
        self._os_platform = platform.system()

    @property
    def default_browser(self) -> str:
        """Get default browser name."""
        return self._default_browser[:-4]

    @property
    def os_platform(self) -> str:
        """Get current os name."""
        return self._os_platform


os_info = OsInfo()
