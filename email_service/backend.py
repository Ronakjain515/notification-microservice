from .sendgrid import send_sendgrid_email
from .smtp import send_smtp_email

class EmailService:
    @staticmethod
    def send_email(to_emails, subject=None, message=None, template_id=None, dynamic_data=None, provider_type=None, cc_emails=None, bcc_emails=None, attachments=None):
        if not isinstance(to_emails, list):
            to_emails = [to_emails]
        if cc_emails and not isinstance(cc_emails, list):
            cc_emails = [cc_emails]
        if bcc_emails and not isinstance(bcc_emails, list):
            bcc_emails = [bcc_emails]
        if attachments and not isinstance(attachments, list):
            attachments = [attachments]

        if provider_type == 'smtp':
            return EmailService._send_smtp_email(to_emails, subject, message, cc_emails, bcc_emails, attachments)
        elif provider_type == 'sendgrid':
            return EmailService._send_sendgrid_email(to_emails, subject, message, template_id, dynamic_data, cc_emails, bcc_emails, attachments)
        else:
            raise ValueError("Invalid provider_type. Expected 'smtp' or 'sendgrid'.")

    @staticmethod
    def _send_smtp_email(to_emails, subject, message, cc_emails=None, bcc_emails=None, attachments=None):
        return send_smtp_email(to_emails, subject, message, cc_emails, bcc_emails, attachments)

    @staticmethod
    def _send_sendgrid_email(to_emails, subject, message, template_id, dynamic_data, cc_emails=None, bcc_emails=None, attachments=None):
        return send_sendgrid_email(to_emails, subject, message, template_id, dynamic_data, cc_emails, bcc_emails, attachments)
