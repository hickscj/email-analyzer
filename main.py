"""
analyze emails for word frequency
"""

import email
import imaplib
import os
from html import unescape
from dotenv import load_dotenv


def write_email_to_file(content):
    with open('email_output.txt', mode='w', encoding='utf-8') as out_file:
        out_file.write(unescape(content))


load_dotenv()
user = os.getenv('IMAP_EMAIL')
password = os.getenv('IMAP_TOKEN')
imap_url = os.getenv('IMAP_SERVER')

connection = imaplib.IMAP4_SSL(imap_url)
connection.login(user, password)

connection.select(os.getenv('INBOX_NAME'))

result, data = connection.search(None, 'ALL')

if result == 'OK':
    for num in data[0].split():
        result, data = connection.uid('fetch', num, '(RFC822)')
        if result == 'OK':
            email_message = email.message_from_bytes(data[0][1])
            print('From:' + email_message['From'])
            print('To:' + email_message['To'])
            print('Date:' + email_message['Date'])
            print('Subject:' + str(email_message['Subject']))
            print('Content:' + str(email_message.get_payload()[0]))
            write_email_to_file(str(email_message['Subject']) + '\n' + str(email_message.get_payload()[0]))
        break

connection.close()
connection.logout()
