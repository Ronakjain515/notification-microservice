import os
from django.core.mail import EmailMessage
import base64
import mimetypes
from utilities.utils import logger

def send_smtp_email(to_emails, subject, message, cc_emails=None, bcc_emails=None, attachments=None):
    """
    Sends an email via SMTP using Django's EmailMessage class.
    
    Parameters:
    - to_emails: List of recipient email addresses.
    - subject: Subject of the email.
    - message: Body of the email in HTML format.
    - cc_emails: (Optional) List of CC email addresses.
    - bcc_emails: (Optional) List of BCC email addresses.
    - attachments: (Optional) List of dictionaries representing file attachments, where each dictionary contains:
        - 'file_name': Name of the file.
        - 'file': Base64 encoded content of the file.
    
    Returns:
    A tuple (success, message, details) where:
    - success: Boolean indicating if the email was sent successfully.
    - message: Message indicating the result of the email sending attempt.
    - details: Additional details (e.g., error message).
    """
    try:
        # Create an EmailMessage object with the provided subject, message, and recipient addresses
        email = EmailMessage(subject, message, os.getenv('DEFAULT_FROM_EMAIL'), to_emails)
        
        # Set the content subtype to HTML
        email.content_subtype = "html"
        
        # Add CC recipients if provided
        if cc_emails:
            email.cc = cc_emails
        
        # Add BCC recipients if provided
        if bcc_emails:
            email.bcc = bcc_emails
        
        # Process and attach files if provided
        if attachments:
            decoded_attachments = []
            for attachment in attachments:
                try:
                    # Extract file name and base64 encoded data
                    file_name = attachment['file_name']
                    base64_data = attachment['file']
                    
                    # Decode the base64 data to get file content
                    file_content = base64.b64decode(base64_data)
                    
                    # Infer the MIME type from the file extension
                    extension = file_name.rsplit('.', 1)[-1].lower()
                    content_type, _ = mimetypes.guess_type(f"file.{extension}")
                    content_type = content_type or 'application/octet-stream'  # Default to 'application/octet-stream' if MIME type cannot be determined

                    # Append the decoded attachment to the list
                    decoded_attachments.append((file_name, file_content, content_type))
                except Exception as e:
                    # Log the error and return a failure response if there's an issue with decoding an attachment
                    return False, str(e), {}

            # Attach each file to the email
            for file_name, file_content, content_type in decoded_attachments:
                email.attach(file_name, file_content, content_type)
        
        # Send the email
        email.send()
        
        # Log success messages
        logger.debug("Email sending process completed.")
        logger.info("Email sent successfully via SMTP.")
        
        # Return success response
        return True, "Email sent successfully via SMTP", {}
    except Exception as e:
        # Log the error if sending the email fails
        logger.error(f"Error sending email: {str(e)}")
        
        # Return failure response with error details
        return False, str(e), {}
