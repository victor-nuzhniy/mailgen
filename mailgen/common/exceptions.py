"""Exceptions for mailgen app."""


class MailGenError(Exception):
    """General exception for app."""


class ClipboardRetrieveDataError(MailGenError):
    """Error retrieving data from clipboard."""
