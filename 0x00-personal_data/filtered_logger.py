#!/usr/bin/env python3
'''
filter_datum module
'''

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, seperator: str) -> str:  # noqa
    ''' returns the log message obfuscated'''
    for f in fields:
        p: str = r'(?<=date_of_birth=)\d{2}/\d{2}/\d{4}' if f == 'date_of_birth' else rf'(?<={f}=)\w+'  # noqa
        message = re.sub(p, redaction, message)
    return message.replace(';', seperator)
