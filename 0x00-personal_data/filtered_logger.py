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
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = '[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s'
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters a log line."""
        msg = super(RedactingFormatter, self).format(record)
        o = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return o
