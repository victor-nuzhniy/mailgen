"""Mail generator module."""
from mailgen.common.app_utilities import abort, add_info_to_logfile, log_errors
from mailgen.common.gui_operations import (
    captcha_verifier,
    email_verifier,
    generator_operations,
)


@log_errors
def mail_generator() -> None:
    """Generate 'proton.me' email account. Save email and password to logfile."""
    generator_operations.open_incognito_proton_page()
    username, password = generator_operations.create_username_password_pare()
    generator_operations.input_username_password_into_form(username, password)

    if generator_operations.is_captcha_verification():
        captcha_verifier.move_sample_to_place()
    elif generator_operations.is_email_verification():
        email_verifier.verify_email()
    else:
        abort('proton.me verification is unavailable. Try later.')

    generator_operations.finish_registration()

    add_info_to_logfile(username, password)


if __name__ == '__main__':
    mail_generator()
