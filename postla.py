import imaplib
import email
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage
import time
import os
from pypdf import PdfReader, PdfWriter

# login and mail data
username = "batla@gmx.at"
password = input("Type PW: ")
imap_server = "imap.gmx.net"
smtp_server_url = "mail.gmx.net"
smtp_port = 465
download_folder = "./download/"

def pdfsplit(subject, attachment_path):
    # make a list of given split points / names
    splitlist=[]
    for x in subject.split()[1:]:
        try:
            number = int(x[:x.find("_")])
        except:
            print("Number not found")
        try:
            name = x[x.find("_")+1:] + str(".pdf")
        except:
            print("Name not found")

        try:
            splitlist.append([number, name])
        except:
            print("Creation of list not possible")

    # adding the starting page for each splitpoint
    temp_number=0
    for x in splitlist:
        if temp_number == 0:
            x.insert(0, 1)
            temp_number = x[1]
        else:
            x.insert(0, temp_number)
            temp_number = x[1]

    # write pdf files
    with open(attachment_path,'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        for x in splitlist:
            for page in reader.pages[x[0]:x[1]+1]:
                writer.add_page(page)

                with open("./upload/" + x[2], 'wb') as output_pdf:
                    writer.write(output_pdf)
                    
            # reset PdfWriter
            writer = PdfWriter()


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
                time.sleep(10)
                if filename is not None:
                    sv_path = os.path.join(download_folder, filename)
                    if not os.path.isfile(sv_path):
                        print(sv_path)
                        fp = open(sv_path, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()

          # download attachment finish

                ####### FUNCTION INSERT ###########
                    pdfsplit(subject, sv_path) 
                    time.sleep(1)

                ###### FUNCTION END ###############

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
                """
                with open("testpdf.pdf", "rb") as f:
                    email_message.add_attachment(
                            f.read(),
                            filename="testpdf.pdf",
                            maintype="application",
                            subtype="pdf"
                            )
                # add attachment finish
                """
                smtp_server = SMTP_SSL(smtp_server_url, port=smtp_port)
                smtp_server.set_debuglevel(1)
                smtp_server.login(username, password)
                smtp_server.sendmail(from_email, to_email, email_message.as_string())

                smtp_server.quit()
            else:
                print("wrong subject")
    else:
        print("status 0")


