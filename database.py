import sqlite3
from sqlite3 import Error


email_table_sql = """CREATE TABLE IF NOT EXISTS email (
    id integer PRIMARY KEY AUTOINCREMENT,
    date_sent text,
    from_email text,
    to_email text,
    subject text,
    content text
);"""


def create_connection(db_file):
    """ create database connection """
    cxn = None

    try:
        cxn = sqlite3.connect(db_file)
        print(sqlite3.version)
        if cxn:
            create_table(cxn, email_table_sql)
    except Error as e:
        print(e)
    finally:
        if cxn:
            cxn.close()


def create_table(cxn, sql):
    try:
        c = cxn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


create_connection('emails.db')
