"""
analyze emails for word frequency
"""

import email
import imaplib
import os
from dotenv import load_dotenv


load_dotenv()
user = os.getenv('IMAP_EMAIL')
password = os.getenv('IMAP_TOKEN')
imap_url = os.getenv('IMAP_SERVER')

connection = imaplib.IMAP4_SSL(imap_url)
connection.login(user, password)

connection.select('trump')

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
        break

connection.close()
connection.logout()


# import imaplib
# import pprint
# import email
#
# imap_host = 'imap.mail.yahoo.com'
# imap_user = 'chadjhicks@yahoo.com'
# imap_pass = 'etzanyzybvxwywyz'
#
# # connect to host using SSL
# imap = imaplib.IMAP4_SSL(imap_host)
#
# # login to server
# imap.login(imap_user, imap_pass)
#
# imap.select('trump')
#
# tmp, data = imap.search(None, 'ALL')
# for num in data[0].split():
#     tmp, data = imap.fetch(num, '(RFC822)')
#     print('Message: {0}\n'.format(num))
#     # pprint.pprint(data[0][1])
#     msg = email.message_from_bytes(data[0][1])
#     str(msg.get_payload()[0])
#
#     break
#
# imap.close()
