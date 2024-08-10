import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Personalization, Content, Cc, Bcc, Attachment
from sendgrid.helpers.mail import FileContent, FileName, FileType
from utilities.utils import logger

def send_sendgrid_email(to_emails, subject, message, template_id, dynamic_data, cc_emails=None, bcc_emails=None, attachments=None):
    mail = Mail()
    mail.from_email = Email(os.getenv('SENDGRID_SENDER_EMAIL'))

    if template_id:
        logger.info(f"Using template ID: {template_id}")
            
        mail.template_id = template_id
        for email in to_emails:
            personalization = Personalization()
            personalization.add_to(To(email))
            if dynamic_data:
                personalization.dynamic_template_data = {}
                for key, value in dynamic_data.items():
                    personalization.dynamic_template_data[key] = value
            if cc_emails:
                for cc_email in cc_emails:
                    personalization.add_cc(Cc(cc_email))
            if bcc_emails:
                for bcc_email in bcc_emails:
                    personalization.add_bcc(Bcc(bcc_email))
            mail.add_personalization(personalization)
            logger.info(f"Added personalization for email: {email}")
    else:
        logger.info("Sending a non-template email.")
        mail.subject = subject
        mail.content = Content("text/html", message if message else "")
        for email in to_emails:
            mail.add_to(To(email))
            logger.info(f"Added recipient: {email}")
        if cc_emails:
            for cc_email in cc_emails:
                mail.add_cc(Cc(cc_email))
                logger.info(f"Added CC recipient: {cc_email}")
        if bcc_emails:
            for bcc_email in bcc_emails:
                mail.add_bcc(Bcc(bcc_email))
                logger.info(f"Added BCC recipient: {bcc_email}")
    
    if attachments:
        logger.info("Adding attachments.")
            
        for attachment in attachments:
            attachment_obj = Attachment(
                FileContent(attachment['file']),
                FileName(attachment['file_name']),
                FileType('application/octet-stream')
            )
            mail.add_attachment(attachment_obj)
            logger.info(f"Attachment added: {attachment['file_name']}")

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(mail)
        logger.info(f"Email sent successfully. Status code: {response.status_code}")
        return response.status_code, response.body, response.headers
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return False, str(e), {}
