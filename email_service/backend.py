import logging
from .sendgrid import send_sendgrid_email
from .smtp import send_smtp_email
from utilities.utils import logger

class EmailService:
    @staticmethod
    def send_email(to_emails, subject=None, message=None, template_id=None, dynamic_data=None, provider_type=None, cc_emails=None, bcc_emails=None, attachments=None):
        try:
            # Ensure lists are used for email addresses and attachments
            if not isinstance(to_emails, list):
                to_emails = [to_emails]
            if cc_emails and not isinstance(cc_emails, list):
                cc_emails = [cc_emails]
            if bcc_emails and not isinstance(bcc_emails, list):
                bcc_emails = [bcc_emails]
            if attachments and not isinstance(attachments, list):
                attachments = [attachments]

            logger.info(f"Sending email. Provider: {provider_type}, To: {to_emails}, Subject: {subject}")

            if provider_type == 'smtp':
                response = EmailService._send_smtp_email(to_emails, subject, message, cc_emails, bcc_emails, attachments)
                logger.info("SMTP email sent successfully.")
                return response
            elif provider_type == 'sendgrid':
                response = EmailService._send_sendgrid_email(to_emails, subject, message, template_id, dynamic_data, cc_emails, bcc_emails, attachments)
                logger.info("SendGrid email sent successfully.")
                return response
            else:
                raise ValueError("Invalid provider_type. Expected 'smtp' or 'sendgrid'.")
        except Exception as e:
            logger.error(f"Error in sending email: {e}")
            return False, str(e), {}

    @staticmethod
    def _send_smtp_email(to_emails, subject, message, cc_emails=None, bcc_emails=None, attachments=None):
        try:
            logger.debug(f"Preparing to send SMTP email. To: {to_emails}, Subject: {subject}")
            response = send_smtp_email(to_emails, subject, message, cc_emails, bcc_emails, attachments)
            logger.debug(f"SMTP email response: {response}")
            return response
        except Exception as e:
            logger.error(f"Error sending SMTP email: {e}")
            return False, str(e), {}

    @staticmethod
    def _send_sendgrid_email(to_emails, subject, message, template_id, dynamic_data, cc_emails=None, bcc_emails=None, attachments=None):
        try:
            logger.debug(f"Preparing to send SendGrid email. To: {to_emails}, Subject: {subject}, Template ID: {template_id}")
            response = send_sendgrid_email(to_emails, subject, message, template_id, dynamic_data, cc_emails, bcc_emails, attachments)
            logger.debug(f"SendGrid email response: {response}")
            return response
        except Exception as e:
            logger.error(f"Error sending SendGrid email: {e}")
            return False, str(e), {}
