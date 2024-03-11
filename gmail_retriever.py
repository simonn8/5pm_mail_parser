# Importing libraries
import imaplib, email
import os
from datetime import datetime
from email.parser import Parser
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('user')
password = os.getenv('GMAIL_PSWD')
imap_url = 'imap.gmail.com'

# Function to get email content part i.e its body part
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

# Function to search for a key value pair
def search(key, value, con):
    result, data = con.search(None, key, '"{}"'.format(value))
    return data

# Function to get the list of emails under this label
def get_emails(result_bytes):
    msgs = [] # all the email data are pushed inside an array
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)

    return msgs

# this is done to make SSL connection with GMAIL
con = imaplib.IMAP4_SSL(imap_url)

# logging the user in
con.login(user, password)

# calling function to check for email under this label
con.select('5pm_dailymail')

# fetching emails from this user "tu**h*****1@gmail.com"
msgs = get_emails(search('FROM', 'newsletter@news.dailymail.co.uk', con))

parser = Parser()
email = parser.parsestr(msgs[0][0][1].decode("utf-8"))

def store_message_in_file(msg):
    email = parser.parsestr(msg.decode("utf-8"))
    # Your input string
    date_string = email["Date"]

    # Convert string to datetime object
    datetime_obj = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z (EST)')
    news_date = datetime_obj.strftime("%y%m%d")
    html_filename = f"data/newsletter_5pm_{news_date}.html"
    if Path(html_filename).exists():
        return
    if email.is_multipart():
        for part in email.walk():
            content_type = part.get_content_type()
            if content_type == "text/html":
                html = part.get_payload(decode=True).decode()
                with open(html_filename, "w") as f:
                    f.write(html)

# Store each html email into a file in the data folder
for msg in msgs:
    store_message_in_file(msg[0][1])