import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, message, sender_email, sender_password, receiver_email):
    try:
        # Validate inputs
        if not all((subject, message, sender_email, sender_password, receiver_email)):
            print("Error: Please provide all required information.")
            return

        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Connect to SMTP server and send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", str(e))

def receive_email(email_address, password, subject=None):
    try:
        # Validate inputs
        if not all((email_address, password)):
            print("Error: Please provide email address and password.")
            return

        # Connect to IMAP server
        with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
            mail.login(email_address, password)
            mail.select('inbox')

            # Search for emails with optional subject filter
            criteria = 'ALL' if not subject else f'(SUBJECT "{subject}")'
            result, data = mail.search(None, criteria)
            email_ids = data[0].split()

            # Fetch and print emails
            for email_id in email_ids:
                result, data = mail.fetch(email_id, '(RFC822)')
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                print('From:', msg['From'])
                print('Subject:', msg['Subject'])
                print('Body:', msg.get_payload())
                
                # Check if the temperature information is in the email body
                if 'temperature' in msg.get_payload().lower():
                    temperature = float(msg.get_payload().split()[-1])
                    if temperature > 24:
                        send_email("Temperature Alert", f"The current temperature is: {temperature}. Would you like to turn on the fan?", sender_email, sender_password, receiver_email)
                        print("Temperature alert email sent.")

        print("Emails retrieved successfully!")
    except Exception as e:
        print("Error receiving email:", str(e))

# Set sender and receiver email addresses and passwords
sender_email = 'spara2301@gmail.com'
sender_password = 'ofki ppfu tcgn lktj'
receiver_email = 'vladtivig@gmail.com'

# Send email
send_email("Test Email", "This is a test email sent from Raspberry Pi.", sender_email, sender_password, receiver_email)

# Receive email
receive_email(sender_email, sender_password, subject="Test Email")
    