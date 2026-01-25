import imaplib
import email
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage
import time

# login and mail data
username = "batla@gmx.at"
password = input("Type PW: ")
imap_server = "imap.gmx.net"
smtp_server_url = "mail.gmx.net"
smtp_port = 465

def duawos(subject):
    if subject == "three":
        print("THREEEEEEE")
    if subject == "two":
        print("TWOOOOOOO")

while True:
    # check inbox for new unseen mail
    time.sleep(5)
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)
    status, messages = imap.select("Inbox")
    _, msgnums = imap.search(None, "UNSEEN")
    
    # if new unseen mail arrived --> get subject and sender address
    if msgnums[0].split():
        print("INCOME")
        for msgnum in msgnums[0].split():
            _, data = imap.fetch(msgnum, "(RFC822)")

            message = email.message_from_bytes(data[0][1])
            subject = message.get('Subject')
            sender = message.get('From')

            duawos(subject)

        # send mail
            from_email = username
            to_email = sender
            email_message = EmailMessage()
            email_message['To'] = to_email
            email_message['From'] = from_email
            email_message['Subject'] = 'dereoida'
            email_message.set_content("Sehr geehrter Hr. Lucifer! deimuada is a gehsteigpanza")

            smtp_server = SMTP_SSL(smtp_server_url, port=smtp_port)
            smtp_server.set_debuglevel(1)
            smtp_server.login(username, password)
            smtp_server.sendmail(from_email, to_email, email_message.as_string())

            smtp_server.quit()
    else:
        print("status 0")


