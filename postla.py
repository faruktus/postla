import imaplib
import email
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage
import time
import os

# login and mail data
username = "batla@gmx.at"
password = input("Type PW: ")
imap_server = "imap.gmx.net"
smtp_server_url = "mail.gmx.net"
smtp_port = 465
download_folder = "./download/"

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

          # download attachment start  
          
            if message.get_content_maintype() != 'multipart':
                continue
            
            for part in message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename=part.get_filename()
                if filename is not None:
                    sv_path = os.path.join(download_folder, filename)
                    if not os.path.isfile(sv_path):
                        print(sv_path)
                        fp = open(sv_path, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()

          # download attachment finish


            duawos(subject)

        # send mail
            if subject.split()[0] == "pdf":
                from_email = username
                to_email = sender
                email_message = EmailMessage()
                email_message['To'] = to_email
                email_message['From'] = from_email
                email_message['Subject'] = 'dereoida'
                email_message.set_content("Sehr geehrter Hr. Lucifer! deimuada is a gehsteigpanza")
                # add attachment start
                with open("testpdf.pdf", "rb") as f:
                    email_message.add_attachment(
                            f.read(),
                            filename="testpdf.pdf",
                            maintype="application",
                            subtype="pdf"
                            )
                # add attachment finish

                smtp_server = SMTP_SSL(smtp_server_url, port=smtp_port)
                smtp_server.set_debuglevel(1)
                smtp_server.login(username, password)
                smtp_server.sendmail(from_email, to_email, email_message.as_string())

                smtp_server.quit()
            else:
                print("wrong subject")
    else:
        print("status 0")


