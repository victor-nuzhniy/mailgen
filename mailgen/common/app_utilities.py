"""Utilites for mailgen app."""
import logging
import string
from random import SystemRandom
from typing import Any, Callable

from mailgen.common.app_typing import BrowserLetterType, OptionsType
from mailgen.common.constants import LOGFILE
from mailgen.common.exceptions import ServiceUnavailableError
from mailgen.common.os_services import OsInfo

cryptogen = SystemRandom()
logger: logging.Logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def randomize(option: OptionsType, length: int) -> str:
    """
    Return random letters in dependence of given options.

    :param option: str Input parameter. Can be
        -p - for letters, numbers and symbols;
        -s - for letters and numbers;
        -l - for letteres only;
        -n - for numbers only;
        -m - for month first digits selection;
        -d - for month day number selection;
        -y - for year selection;
    :param length: int Number of iteration.

    :return: str Randomized string, empty string or 'error'.
    """
    options: dict = {
        '-p': '{letters}{digits}{symbols}'.format(
            letters=string.ascii_letters,
            digits=string.digits,
            symbols='!@#$%^&*()_+',
        ),
        '-s': '{letters}{digits}'.format(
            letters=string.ascii_letters,
            digits=string.digits,
        ),
        '-l': string.ascii_letters,
        '-n': string.digits,
        '-m': 'JFMASOND',
        '-d': str(cryptogen.randrange(1, 28)),
        '-y': str(cryptogen.randrange(1950, 2000)),
    }
    if length:
        sample_string: str = options.get(option, '')
        return ''.join(cryptogen.choice(sample_string) for _ in range(length))
    return 'error'


def add_info_to_logfile(username: str, password: str) -> None:
    """Write usename and password to logfile."""
    logger.info('{name}@proton.me:{word}'.format(name=username, word=password))
    with open(LOGFILE, 'a') as log_file:
        log_file.write(
            '{username}@proton.me:{password}\n'.format(
                username=username,
                password=password,
            ),
        )


def abort(text: str) -> None:
    """Raise ServiceUnavailableError."""
    raise ServiceUnavailableError(text)


def log_errors(func: Callable) -> Callable:
    """Wrap func with catching errors functionality."""

    def wrap(*args: Any, **kwargs: Any) -> Any:  # noqa: WPS430
        try:
            return func(*args, **kwargs)
        except ServiceUnavailableError as ex:
            logger.info(str(ex))

    return wrap


def get_incognito_open_tab_letter() -> BrowserLetterType:
    """Get specific browser hot key letter to open incognito tab."""
    os_info = OsInfo()
    if os_info.default_browser == 'firefox':
        return 'p'
    return 'n'
