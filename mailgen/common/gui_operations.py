"""Auto gui operations for mailgen app."""
import logging
import time
import webbrowser

import pyautogui

from mailgen.common.app_services import WindllService, search_email, search_six_digits
from mailgen.common.app_utilities import randomize
from mailgen.common.constants import DROPMAIL_URL, GOOGLE_URL, PROTON_URL

windll_service = WindllService()
logger: logging.Logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class EmailVerifier(object):
    """Class with gui email verification functionality."""

    def check_email(self) -> None:
        """Get email to verify 'proton.me' account."""
        new_mail = 'some_email'
        while True:
            if not new_mail:
                pyautogui.hotkey('ctrl', 'r')
                time.sleep(4)
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

    def find_email_and_use_for_verification(self) -> None:  # noqa: WPS213
        """Find email with given service and use for verification."""
        pyautogui.typewrite('\t\t\t\n')

        pyautogui.hotkey('ctrl', 't')

        time.sleep(3)
        pyautogui.typewrite('{url}\n'.format(url=DROPMAIL_URL))

        self.check_email()

        pyautogui.hotkey('ctrl', '\t')
        time.sleep(1)

        pyautogui.hotkey('ctrl', 'v')

        pyautogui.typewrite('\n')

    def copy_to_clipboard_dropmail_page(self) -> None:
        """Copy to clipboard 'dropmail.me' page."""
        time.sleep(25)

        pyautogui.hotkey('ctrl', '\t')
        time.sleep(5)
        pyautogui.typewrite('\t\t\t\t\t\t')
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'c')

    def use_verification_digit_from_clipboard(self) -> None:
        """Use previously saved to clipboard verification digits."""
        time.sleep(0.1)
        pyautogui.hotkey('shift', '\t')
        pyautogui.hotkey('ctrl', '\t')
        time.sleep(5)
        six_digits: str = windll_service.get_clipboard_data(search_six_digits)

        pyautogui.typewrite('{digits}\n'.format(digits=six_digits))

        time.sleep(5)
        pyautogui.typewrite('\n')

    def verify_email(self) -> None:
        """Verify proton accaunt with email verification."""
        self.find_email_and_use_for_verification()
        self.copy_to_clipboard_dropmail_page()
        self.use_verification_digit_from_clipboard()


email_verifier = EmailVerifier()


class GeneratorOperations(object):
    """Class with generator gui functionality."""

    def open_incognito_proton_page(self) -> None:
        """Open incognito tab, previously opend google page."""
        webbrowser.open(GOOGLE_URL)

        time.sleep(5)

        pyautogui.hotkey('ctrlleft', 'shift', 'n')  # add logic default browser
        pyautogui.typewrite('{url}\n'.format(url=PROTON_URL))
        time.sleep(5)

    def create_username_password_pare(self) -> tuple[str, str]:
        """Create username and password."""
        username: str = ''.join(randomize('-s', 5) for _ in range(3))
        logger.info('Username: {name}'.format(name=username))
        password = randomize('-p', 16)
        logger.info('Password: {word}'.format(word=password))
        return username, password

    def input_username_password_into_form(self, username: str, password: str) -> None:
        """Input username and password into form."""
        pyautogui.typewrite('{name}\t\t\t'.format(name=username))
        time.sleep(0.6)
        pyautogui.typewrite(
            '{first}\t{second}\t'.format(first=password, second=password),
        )
        time.sleep(0.6)
        pyautogui.typewrite('\n')
        time.sleep(5)

    def finish_registration(self) -> None:
        """Finish registration, refusing to use phone number as verification."""
        time.sleep(5)
        pyautogui.typewrite('\t\t\t\n')
        time.sleep(1)
        pyautogui.typewrite('\t\n')


generator_operations = GeneratorOperations()
