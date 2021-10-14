"""
download emails from server and save for analysis
"""

import email
import imaplib
import os
import re
import sqlite3
from sqlite3 import Error

from dotenv import load_dotenv

db_file = 'emails.db'


def write_email_to_file(content, output_file):
    with open('data/' + output_file, mode='w', encoding='utf-8') as out_file:
        out_file.write(content)


def write_email_to_database(message):
    cxn = None
    try:
        cxn = sqlite3.connect(db_file)
        print(sqlite3.version)
        if cxn:
            variables = [message['Date'], message['From'], message['To'],
                         str(message['Subject']), str(message.get_payload()[0])]
            cxn.execute("INSERT INTO email (date_sent, from_email, to_email, subject, content) VALUES (?, ?, ?, ?, ?)",
                        variables)
            cxn.commit()
    except Error as e:
        print(e)
    finally:
        if cxn:
            cxn.close()


def download_emails():
    load_dotenv()
    user = os.getenv('IMAP_EMAIL')
    password = os.getenv('IMAP_TOKEN')
    imap_url = os.getenv('IMAP_SERVER')

    try:
        connection = imaplib.IMAP4_SSL(imap_url)
        connection.login(user, password)

        connection.select(os.getenv('INBOX_NAME'))

        result, data = connection.search(None, 'ALL')

        if result == 'OK':
            for num in data[0].split():
                result, data = connection.uid('fetch', num, '(RFC822)')
                if result == 'OK':
                    email_message = email.message_from_bytes(data[0][1])
                    email_output = 'From:' + email_message['From'] + '\n'
                    email_output += 'To:' + email_message['To'] + '\n'
                    email_output += 'Date:' + email_message['Date'] + '\n'
                    email_output += 'Subject:' + str(email_message['Subject']) + '\n'
                    email_output += 'Content:' + str(email_message.get_payload()[0]) + '\n'
                    file_name = re.sub("[?!*']", '', str(email_message['Subject'])
                                       .lower().strip().replace(' ', '_')) + '.txt'
                    # write_email_to_file(email_output, file_name)
                    write_email_to_database(email_message)
                    break

        connection.close()
        connection.logout()

    except ConnectionError:
        print('Error with email server connection')


download_emails()
