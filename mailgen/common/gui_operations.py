"""Auto gui operations for mailgen app."""
import logging
import time

import pyautogui

from mailgen.common.app_services import WindllService, search_email, search_six_digits
from mailgen.common.constants import DROPMAIL_URL

windll_service = WindllService()
logger: logging.Logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def check_email() -> None:
    """Get email to verify 'proton.me' account."""
    new_mail = 'some_email'
    while True:
        if not new_mail:
            pyautogui.hotkey('ctrl', 'r')
            time.sleep(5)
        box_object = pyautogui.locateCenterOnScreen(
            'mailgen/images/copy_icon.png',
            confidence=0.7,
        )
        time.sleep(2)
        if box_object:
            xx, yy = box_object
            pyautogui.click(xx, yy)
            time.sleep(1)
            new_mail = windll_service.get_clipboard_data(search_email)
            if new_mail:
                logger.info('10 min mail: {email}'.format(email=new_mail))
                break


def find_email_and_use_for_verification() -> None:  # noqa: WPS213
    """Find email with given service and use for verification."""
    pyautogui.typewrite('\t\t\t\n')

    pyautogui.hotkey('ctrl', 't')

    time.sleep(10)
    pyautogui.typewrite('{url}\n'.format(url=DROPMAIL_URL))

    check_email()

    pyautogui.hotkey('ctrl', '\t')
    time.sleep(1)

    pyautogui.hotkey('ctrl', 'v')

    pyautogui.typewrite('\n')


def copy_to_clipboard_dropmail_page() -> None:
    """Copy to clipboard 'dropmail.me' page."""
    time.sleep(25)

    pyautogui.hotkey('ctrl', '\t')
    time.sleep(5)

    pyautogui.typewrite('\t')
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'c')


def use_verification_digit_from_clipboard() -> None:
    """Use previously saved to clipboard verification digits."""
    time.sleep(0.1)
    pyautogui.hotkey('shift', '\t')
    pyautogui.hotkey('ctrl', '\t')
    time.sleep(5)
    six_digits: str = windll_service.get_clipboard_data(search_six_digits)

    pyautogui.typewrite('{digits}\n'.format(digits=six_digits))

    time.sleep(5)
    pyautogui.typewrite('\n')


def email_verification() -> None:
    """Verify proton accaunt with email verification."""
    find_email_and_use_for_verification()
    copy_to_clipboard_dropmail_page()
    use_verification_digit_from_clipboard()
