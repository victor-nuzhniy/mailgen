"""Mail generator module."""
from mailgen.common.app_utilities import add_info_to_logfile
from mailgen.common.gui_operations import email_verifier, generator_operations


def mail_generator() -> None:
    """Generate 'proton.me' email account. Save email and password to logfile."""
    generator_operations.open_incognito_proton_page()
    username, password = generator_operations.create_username_password_pare()
    generator_operations.input_username_password_into_form(username, password)

    # decide what verification to chose
    email_verifier.verify_email()
    # end email verification

    generator_operations.finish_registration()

    add_info_to_logfile(username, password)


if __name__ == '__main__':
    mail_generator()
