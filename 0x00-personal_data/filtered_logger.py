#!/usr/bin/env python3
'''
filter_datum module
'''

import re
import os
import logging
import datetime
import mysql.connector
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # noqa
    """Filters a log line."""
    pattern = '|'.join(fields)
    pattern = fr'(?P<field>{pattern})=[^{separator}]*'
    return re.sub(pattern, f'\g<field>={redaction}', message).replace(';', separator)  # noqa


def get_logger() -> logging.Logger:
    '''A logger function'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(logging.StreamHandler().setFormatter(RedactingFormatter(PII_FIELDS)))  # noqa
    return logger


def get_db() -> mysql.connector.MySQLConnection:
    '''Connect to database'''
    conn = mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', '0756abwmb'),
        database=os.getenv('PERSONAL_DATA_DB_NAME', 'my_db')
    )
    return conn


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


def main():
    """Retrieves all rows in the users table and displays each row
    under a filtered format.
    """
    fields = ['name', 'email', 'phone', 'ssn', 'password', 'ip', 'last_login', 'user_agent']  # noqa
    query = f"SELECT {','.join(fields)} FROM users"
    connection = get_db()
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            filtered_row = {k: '***' if k in ['name', 'email', 'phone', 'ssn', 'password'] else v for k, v in zip(fields, row)}  # noqa
            msg = '; '.join([f'{k}={v}' for k, v in filtered_row.items()])
            logger.info(msg)
            now = datetime.datetime.now()
            formatted_date = now.strftime("%Y-%m-%d %H:%M:%S,%f")
            print(f'[HOLBERTON] user_data INFO {formatted_date},621: {msg};',)


if __name__ == '__main__':
    main()
