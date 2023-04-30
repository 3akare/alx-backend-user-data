#!/usr/bin/env python3
'''
filter_datum module
'''

import re
from typing import List


def filter_datum(fields: str, redaction: str, message: List[str], seperator: str) -> str:  # noqa
    ''' returns the log message obfuscated'''
    for f in fields:
        p: str = r'(?<=date_of_birth=)\d{2}/\d{2}/\d{4}' if f == 'date_of_birth' else rf'(?<={f}=)\w+'  # noqa
        message = re.sub(p, redaction, message)
    return message.replace(';', seperator)

fields = ["password", "date_of_birth"]
messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))