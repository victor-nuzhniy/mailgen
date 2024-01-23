"""Utilites for mailgen app."""
import string
from random import SystemRandom

from mailgen.common.app_typing import OptionsType

cryptogen = SystemRandom()


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
