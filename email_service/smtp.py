import os
from django.core.mail import EmailMessage
import base64
import mimetypes
from utilities.utils import logger

def send_smtp_email(to_emails, subject, message, cc_emails=None, bcc_emails=None, attachments=None):
    try:
        email = EmailMessage(subject, message, os.getenv('DEFAULT_FROM_EMAIL'), to_emails)
        email.content_subtype = "html"  # Main content is now text/html
        if cc_emails:
            email.cc = cc_emails
        if bcc_emails:
            email.bcc = bcc_emails
        if attachments:
            decoded_attachments = []
            for attachment in attachments:
                try:
                    file_name = attachment['file_name']
                    base64_data = attachment['file']
                    file_content = base64.b64decode(base64_data)
                    
                    
                    # Infer MIME type from file extension
                    extension = file_name.rsplit('.', 1)[-1].lower()
                    content_type, _ = mimetypes.guess_type(f"file.{extension}")
                    content_type = content_type or 'application/octet-stream'

                    decoded_attachments.append((file_name, file_content, content_type))
                except Exception as e:
                    return False, str(e), {}

            for file_name, file_content, content_type in decoded_attachments:
                email.attach(file_name, file_content, content_type)
        
        email.send()
        logger.debug("Debug message from some_function")
        logger.info("Email sent successfully via SMTP.")
        return True, "Email sent successfully via SMTP", {}
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return False, str(e), {}
