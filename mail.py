import imaplib
import email
import re

async def extract_code():
    email_address = 'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX'
    password = 'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX'
    IMAP_SERVER = 'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX'
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(email_address, password)
    mail.select('inbox')

    result, data = mail.search(None, '(FROM "XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX")')

    latest_email_id = data[0].split()[-1]
    result, data = mail.fetch(latest_email_id, '(XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX)')

    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    email_body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            try:
                email_body += part.get_payload(decode=True).decode()
            except:
                pass
    else:
        email_body = msg.get_payload(decode=True).decode()

    code_match = re.search(r'код (\d{4,5})', email_body, re.IGNORECASE)
    if code_match:
        code = code_match.group(1)
        return code

    mail.close()
    mail.logout()
