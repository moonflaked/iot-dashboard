import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from enum import Enum, auto
email_sent = False
email_sent_intensity = False
response_received = False
yes_response_received = False


class EmailSentSelect(Enum):
    FAN_EMAIL_SEND = auto(),
    INTENSITY_EMAIL_SEND = auto()

def send_email(email, password, text, sender_email, receiver_email, email_sent_type=EmailSentSelect.FAN_EMAIL_SEND):
    global email_sent
    global email_sent_intensity
    if(email_sent_type == EmailSentSelect.FAN_EMAIL_SEND and email_sent == False):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        server.login(email, password)
        
        server.sendmail(sender_email, receiver_email, msg=text)
        server.quit()
    elif(email_sent_type == EmailSentSelect.INTENSITY_EMAIL_SEND and email_sent_intensity == False): 
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        server.login(email, password)
        server.sendmail(sender_email, receiver_email, msg=text)
        print(text)
        server.quit()
        

def receive_email(email_address, password, subject=None):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(email_address, password)
    imap.select("inbox")

    # Search for unseen emails in the inbox using the specified criteria
    # .search returns two tuples, including status code and the message IDs separated by spaces
    typ, data = imap.search(None, "UNSEEN")
    if(not data[0]):
        return
    latest_message_id = data[0].split()[-1]
    # Fetch the content of the latest message received using the message ID's from .search
    typ, data = imap.fetch(latest_message_id, "(RFC822)")
    
    raw_email = data[0][1]
    # Return a message from a byte-like structure
    msg = email.message_from_bytes(raw_email)
    payload = ""
    if msg.is_multipart():
        for part in msg.walk():
            try:
                imap.store(latest_message_id, "+FLAGS", "\Seen")
                payload = part.get_payload(decode=True).decode()
                break
                #print("Body: " + body)
            except:
                print("Error when getting the body of the message")
    else:
        imap.store(latest_message_id, "+FLAGS", "\Seen")
        payload = part.get_payload(decode=True).decode()
        #print("Body: " + body)
    imap.close()
    imap.logout()
    return payload
    