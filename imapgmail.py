import imaplib
import email
import quopri
from twilio.rest import Client
from dotenv import load_dotenv
import os
import time

load_dotenv()

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)


imap_server = "imap.gmail.com"
email_address = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

while True:
    try:
        imap = imaplib.IMAP4_SSL(imap_server, port=993)
        imap.login(email_address, password)
        imap.select("INBOX")

        _, msg_numbers = imap.search(None, "UNSEEN")

        for msgnum in msg_numbers[0].split():
            _, data = imap.fetch(msgnum, "(RFC822)")

            messageimap = email.message_from_bytes(data[0][1])
            message_date = messageimap.get("Date")
            message_subject = messageimap.get("Subject")
            sender = messageimap.get('From')

            print(f"Message Number: {msgnum}")
            print(f"From: {sender}")
            print(f"Date: {message_date}")
            print(f"Subject: {message_subject}")

            message_content = ""
            for part in messageimap.walk():
                if part.get_content_type() == "text/plain":
                    raw_content = part.get_payload(decode=True)
                    decoded_content = quopri.decodestring(raw_content).decode('utf-8')
                    message_content += decoded_content.replace('=0D=0A', '\n')

            # Construct the message_body within the loop
            message_body = f"Date of Mail: {message_date}\nSubject: {message_subject}\nContent: {message_content[:500]}........"  # Truncated content
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=message_body,
                to=os.getenv('MY_NUM')
            )
            print(f"Message SID: {message.sid}")

        imap.close()
        time.sleep(1500)  # Sleep outside the inner loop
    except Exception as e:
        print(f"An error occurred: {e}")

