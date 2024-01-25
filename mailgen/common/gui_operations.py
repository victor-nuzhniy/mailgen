"""Auto gui operations for mailgen app."""
import logging
import time
import webbrowser
from typing import Optional

import pyautogui

from mailgen.common.app_services import WindllService, app_searchers
from mailgen.common.app_utilities import abort, get_incognito_open_tab_letter, randomize
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
                time.sleep(0.9)
                new_mail = windll_service.get_clipboard_data(app_searchers.search_email)
                if new_mail:
                    logger.info('10 min mail: {email}'.format(email=new_mail))
                    break

    def find_email_and_use_for_verification(self) -> None:  # noqa: WPS213
        """Find email with given service and use for verification."""
        pyautogui.typewrite('\t\t\t\t\t')
        pyautogui.hotkey('ctrl', 't')
        time.sleep(3)
        pyautogui.typewrite('{url}\n'.format(url=DROPMAIL_URL))

        self.check_email()

        pyautogui.hotkey('ctrl', '\t')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.4)
        pyautogui.typewrite('\n')

    def is_email_correct(self) -> None:
        """Check whether email accepted as available for verification."""
        time.sleep(1)
        pyautogui.click(x=0, y=300)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.9)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(2)
        pyautogui.click(x=0, y=300)
        if windll_service.get_clipboard_data(app_searchers.search_email_verif_phrase):
            abort('Verification email was not accepted. Try again.')

    def copy_to_clipboard_dropmail_page(self) -> None:
        """Copy to clipboard 'dropmail.me' page."""
        time.sleep(25)
        pyautogui.hotkey('ctrl', '\t')
        time.sleep(5)
        pyautogui.click(0, 300)
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'c')

    def use_verification_digit_from_clipboard(self) -> None:  # noqa: WPS213
        """Use previously saved to clipboard verification digits."""
        time.sleep(0.1)
        pyautogui.hotkey('shift', '\t')
        pyautogui.hotkey('ctrl', '\t')
        time.sleep(5)
        pyautogui.typewrite('\t\t')
        six_digits: str = windll_service.get_clipboard_data(
            app_searchers.search_six_digits,
        )
        if not six_digits:
            abort("Digits haven't received to verification email. Try again.")
        pyautogui.typewrite('{digits}\n'.format(digits=six_digits))
        time.sleep(3)
        pyautogui.typewrite('\n')

    def verify_email(self) -> None:
        """Verify proton accaunt with email verification."""
        self.find_email_and_use_for_verification()
        self.is_email_correct()
        self.copy_to_clipboard_dropmail_page()
        self.use_verification_digit_from_clipboard()


email_verifier = EmailVerifier()


class GeneratorOperations(object):
    """Class with generator gui functionality."""

    def open_incognito_proton_page(self) -> None:
        """Open incognito tab, previously opend google page."""
        webbrowser.open(GOOGLE_URL)

        time.sleep(5)
        letter = get_incognito_open_tab_letter()
        pyautogui.hotkey('ctrlleft', 'shift', letter)  # add logic default browser
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
        time.sleep(15)
        pyautogui.typewrite('\t\t\t\n')
        time.sleep(1)
        pyautogui.typewrite('\t\n')

    def is_captcha_verification(self) -> bool:
        """Check, whether captcha verification available."""
        pyautogui.click(0, 300)
        time.sleep(0.4)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        pyautogui.click(x=0, y=300)
        return bool(
            windll_service.get_clipboard_data(app_searchers.search_captcha_word),
        )

    def is_email_verification(self) -> bool:
        """Check, whether email verification available."""
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        pyautogui.click(x=0, y=300)
        return bool(windll_service.get_clipboard_data(app_searchers.search_email_word))


generator_operations = GeneratorOperations()


class CaptchaVerifier(object):
    """Class with gui captcha verification functionality."""

    def move_sample_to_place(self) -> None:  # noqa: WPS213
        """Move captcha sample to place."""
        coordinates: Optional[tuple] = self.get_sample_and_place_location()
        if not coordinates:
            abort(
                ''.join(
                    (
                        "Account verification failed - haven'nt found CAPTCHA samples.",
                        ' Try again',
                    ),
                ),
            )
        xx, yy, xxx, yyy = coordinates  # type: ignore
        pyautogui.moveTo(xx, yy)
        time.sleep(2)
        pyautogui.dragTo(xxx + 2, yyy - 3, 2, button='left')
        time.sleep(2)
        pyautogui.leftClick(0, 300)
        time.sleep(0.3)
        pyautogui.press('enter')  # TODO check , add tabs
        time.sleep(20)
        if generator_operations.is_captcha_verification():
            abort('CAPTCHA verification failed. Please, try again.')

    def get_sample_and_place_location(self) -> Optional[tuple[int, int, int, int]]:
        """Get captcha sample and place location."""
        sample = pyautogui.locateCenterOnScreen(
            'mailgen/images/captcha_sample.png',
            confidence=0.5,
            grayscale=True,
        )
        time.sleep(3)
        place = pyautogui.locateCenterOnScreen(
            'mailgen/images/captcha_place.png',
            confidence=0.7,
            grayscale=True,
        )
        time.sleep(3)
        if sample and place:
            return sample + place
        return None


captcha_verifier = CaptchaVerifier()
