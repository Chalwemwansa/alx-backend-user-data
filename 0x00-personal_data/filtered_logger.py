#!/usr/bin/env python3
"""module contains a function called filter_datum that
returns the log message obfuscated"""
from typing import List, Tuple
import re
import logging
import os
import mysql.connector


PII_FIELDS: Tuple[str] = ("name", "email", "phone", "ssn", "password",)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        that contains necessary data for formatting the log messages"""

    REDACTION: str = "***"
    FORMAT: str = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: \
%(message)s"
    SEPARATOR: str = ";"

    def __init__(self, fields: List[str]) -> None:
        """constructor for RedactingFormatter"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """this function filters values in incoming log records
        using filter_datum"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 seperator: str) -> str:
    """returns the log message obfuscated, uses a regex to replace
    occurences of certain fields with certain values"""
    for field in fields:
        message = re.sub(rf'{field}=(.*?){seperator}',
                         f'{field}={redaction}{seperator}', message)
    return message


def get_logger() -> logging.Logger:
    """function that returns a logging.Logger object with a list of field in
        PII_FIELDS obfuscated"""
    logger: logging.Logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream: logging.StreamHandler = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """function that returns a connector to the database and
    uses different environment variables to connect to the database"""
    return mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME'))
