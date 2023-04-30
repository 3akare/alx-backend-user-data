#!/usr/bin/env python3
'''
filter_datum module
'''

import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # noqa
    """Filters a log line."""
    pattern = '|'.join(fields)
    pattern = fr'(?P<field>{pattern})=[^{separator}]*'
    return re.sub(pattern, f'\g<field>={redaction}', message).replace(';', separator)  # noqa


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Filters a log line."""
        return filter_datum(self.fields, self.REDACTION, super(RedactingFormatter, self).format(record), self.SEPARATOR)  # noqa
