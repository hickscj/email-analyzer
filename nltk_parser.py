from nltk import data, download, sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import re

try:
    data.find('tokenizers/punkt')
except LookupError:
    download('punkt')


def analyze_text(text):
    tokenized_text = word_tokenize(text)
    fdist = FreqDist(tokenized_text)

    for tup in fdist.most_common():
        if len(tup[0]) > 1 and tup[1] > 1:
            print(tup)


def clean_up_text(text):
    replacers = [
        (r'\n', ' '),
        (r'&\s?z\s?w\s?n\s?j\s?;', ''),
        (r'&rsquo;', "'"),
        (r'=2E', '.'),
        (r'=20', ''),
        (r'[a-zA-Z0-9]{30,}', ''),
        (r'\s{2,}', ' ')
    ]
    for pattern in replacers:
        text = re.sub(pattern[0], pattern[1], text)

    # saved_line = re.sub(r'\n', ' ', saved_line)
    # saved_line = re.sub(r'&\s?z\s?w\s?n\s?j\s?;', '', saved_line)
    # saved_line = re.sub(r'&rsquo;', "'", saved_line)
    # saved_line = re.sub(r'=2E', '.', saved_line)
    # saved_line = re.sub(r'=20', '', saved_line)
    # saved_line = re.sub(r'[a-zA-Z0-9]{30,}', '', saved_line)
    # saved_line = re.sub(r'\s{2,}', ' ', saved_line)  # collapse whitespace
    return text


def squash_email(email_file_name):
    with open(email_file_name, mode='r', encoding='utf-8') as text:
        saved_line = ''
        for idx, line in enumerate(text):
            line = re.sub(r'=\n', '', line)
            line = line.strip()
            saved_line += ' ' + line

        # print(saved_line)

        saved_line = clean_up_text(saved_line)
        analyze_text(saved_line)


squash_email('data/email_output.txt')
