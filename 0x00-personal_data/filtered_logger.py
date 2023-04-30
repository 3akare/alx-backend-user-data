#!/usr/bin/env python3
'''
filter_datum module
'''

import re


def filter_datum(fields, redaction, message, seperator):
    ''' returns the log message obfuscated'''
    for f in fields:
        p = rf'''(?<={f}=)\w+|(?<=date_of_birth=)\d{{2}}/\d{{2}}/\d{{4}}'''
        message = re.sub(p, redaction, message)
    return message.replace(';', seperator)
