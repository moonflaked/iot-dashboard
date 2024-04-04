import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

email_sent = False
response_received = False
yes_response_received = False

def send_email(email, password, text, sender_email, receiver_email):
    
    if email_sent == False: 
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        print("after smtp function")
        server.starttls()
        
        server.login(email, password)
        
        server.sendmail(sender_email, receiver_email, text)
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
    