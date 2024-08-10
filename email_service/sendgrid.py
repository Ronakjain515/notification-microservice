import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Personalization, Content, Cc, Bcc, Attachment
from sendgrid.helpers.mail import FileContent, FileName, FileType
from utilities.utils import logger

def send_sendgrid_email(to_emails, subject, message, template_id, dynamic_data, cc_emails=None, bcc_emails=None, attachments=None):
    """
    Sends an email using SendGrid's API.
    
    Parameters:
    - to_emails: List of recipient email addresses.
    - subject: Subject of the email (used if not using a template).
    - message: Body of the email (used if not using a template).
    - template_id: (Optional) ID of the SendGrid template to use.
    - dynamic_data: (Optional) Data to populate dynamic fields in the SendGrid template.
    - cc_emails: (Optional) List of CC email addresses.
    - bcc_emails: (Optional) List of BCC email addresses.
    - attachments: (Optional) List of dictionaries representing file attachments.
    
    Returns:
    A tuple (status_code, response_body, response_headers) where:
    - status_code: HTTP status code of the response.
    - response_body: Body of the response.
    - response_headers: Headers of the response.
    """
    
    # Create a new Mail object
    mail = Mail()
    
    # Set the sender email address
    mail.from_email = Email(os.getenv('SENDGRID_SENDER_EMAIL'))

    # If a template ID is provided, configure the email for template usage
    if template_id:
        logger.info(f"Using template ID: {template_id}")
        
        mail.template_id = template_id
        for email in to_emails:
            # Create a Personalization object for each recipient
            personalization = Personalization()
            personalization.add_to(To(email))
            
            # Add dynamic data to the template, if provided
            if dynamic_data:
                personalization.dynamic_template_data = {}
                for key, value in dynamic_data.items():
                    personalization.dynamic_template_data[key] = value
            
            # Add CC recipients if provided
            if cc_emails:
                for cc_email in cc_emails:
                    personalization.add_cc(Cc(cc_email))
            
            # Add BCC recipients if provided
            if bcc_emails:
                for bcc_email in bcc_emails:
                    personalization.add_bcc(Bcc(bcc_email))
            
            # Add personalization to the mail object
            mail.add_personalization(personalization)
            logger.info(f"Added personalization for email: {email}")
    else:
        # If no template is used, configure the email with subject and content
        logger.info("Sending a non-template email.")
        mail.subject = subject
        mail.content = Content("text/html", message if message else "")
        
        # Add each recipient to the email
        for email in to_emails:
            mail.add_to(To(email))
            logger.info(f"Added recipient: {email}")
        
        # Add CC recipients if provided
        if cc_emails:
            for cc_email in cc_emails:
                mail.add_cc(Cc(cc_email))
                logger.info(f"Added CC recipient: {cc_email}")
        
        # Add BCC recipients if provided
        if bcc_emails:
            for bcc_email in bcc_emails:
                mail.add_bcc(Bcc(bcc_email))
                logger.info(f"Added BCC recipient: {bcc_email}")

    # Add attachments if provided
    if attachments:
        logger.info("Adding attachments.")
        
        for attachment in attachments:
            # Create an Attachment object for each file
            attachment_obj = Attachment(
                FileContent(attachment['file']),
                FileName(attachment['file_name']),
                FileType('application/octet-stream')  # Default MIME type
            )
            mail.add_attachment(attachment_obj)
            logger.info(f"Attachment added: {attachment['file_name']}")

    try:
        # Create a SendGrid API client using the API key
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        
        # Send the email and get the response
        response = sg.send(mail)
        
        # Log the successful email send
        logger.info(f"Email sent successfully. Status code: {response.status_code}")
        return response.status_code, response.body, response.headers
    except Exception as e:
        # Log any errors that occur during email sending
        logger.error(f"Error sending email: {str(e)}")
        return False, str(e), {}
