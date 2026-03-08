import imaplib
import email
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage
import time
import sys, os
from pypdf import PdfReader, PdfWriter


# login and mail data
username = "batla@gmx.at"
password = input("PW: ")
imap_server = "imap.gmx.net"
smtp_server_url = "mail.gmx.net"
smtp_port = 465
download_folder = "./download/"

# V V V V V V V V V V V V V
### DEFINE FANCY SCRIPT ###

def pdfsplit(splitlist, attachment_path):
    page_dict={}
    for x in splitlist:
        colon_pos = x.find(':')
        hyphen_pos = x.find('-')

        title = x[:colon_pos]
        firstnumber = int(x[(colon_pos+2):hyphen_pos].strip()) - 1
        secondnumber = int(x[(hyphen_pos+1):].strip()) 

        page_dict[title] = [firstnumber, secondnumber]

    with open(attachment_path,'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        for k, v in page_dict.items():
            for page in reader.pages[v[0]:v[1]]:
                writer.add_page(page)

                with open("./upload/" + k + ".pdf", 'wb') as output_pdf:
                    writer.write(output_pdf)

            writer = PdfWriter()

### END OF SCRIPT DEFINITION ### 
# ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^  


# >>>>>>>>>>>>>>>>> STARTING MAIL OPERATIONS <<<<<<<<<<<<<<<<<<<<<<<<

def get_text(msg):
    if msg.is_multipart():
        return get_text(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)
    
# check inbox for new unseen mail
while True:
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
            body = str(get_text(message), 'utf-8')
            subject = message.get('Subject')
            sender = message.get('From')
            
          # V V V V V V V V V V V V V
          # download attachment start  
          
            if message.get_content_maintype() != 'multipart':
                continue
            
            for part in message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                # get Mail Text / Split Points
                splitpoint_list = body.split("\n")
                splitpoints = [x.strip('\r') for x in splitpoint_list if x and x != '\r']

                filename = part.get_filename()
                if filename is not None:
                    sv_path = os.path.join(download_folder, filename)
                    if not os.path.isfile(sv_path):
                        fp = open(sv_path, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()

          # download attachment finish
          # ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 

                    ###### FUNCTION INSERT ###########
                    pdfsplit(splitpoints, sv_path) 
                    ###### FUNCTION END ###############

            # send mail
            if subject.split()[0] == "pdf":
                from_email = username
                to_email = sender
                email_message = EmailMessage()
                email_message['To'] = to_email
                email_message['From'] = from_email
                email_message['Subject'] = 'dere oida'
                email_message.set_content("Vanülle schmeckt vui noch Weihnochtn!")

                #  V V V V V V V V V V
                # add attachment start
                upload_folder = os.listdir("./upload")
                if "NONE" in upload_folder:
                    upload_folder.remove("NONE")
               
                for pdfname in upload_folder:
                    with open("./upload/" + pdfname, "rb") as f:
                        email_message.add_attachment(
                                f.read(),
                                filename=pdfname,
                                maintype="application",
                                subtype="pdf"
                                )
                # add attachment finish
                # ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 

                # delete files from folder download and upload
                for filename in os.listdir("./upload"):
                    os.remove("./upload/" + filename)

                for filename in os.listdir("./download"):
                    os.remove("./download/" + filename)

                # create NONE for easier github interaction
                open('./download/NONE', 'a').close()
                open('./upload/NONE', 'a').close()
                

                smtp_server = SMTP_SSL(smtp_server_url, port=smtp_port)
                smtp_server.set_debuglevel(1)
                smtp_server.login(username, password)
                smtp_server.sendmail(from_email, to_email, email_message.as_string())

                smtp_server.quit()
            else:
                print("wrong subject")
    else:
        print("Checking Inbox...")
