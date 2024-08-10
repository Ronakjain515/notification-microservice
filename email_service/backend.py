import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Personalization, Content, Cc, Bcc, Attachment
from sendgrid.helpers.mail import FileContent, FileName, FileType
from django.core.mail import EmailMessage
import base64
import mimetypes

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
            return True, "Email sent successfully via SMTP", {}
        except Exception as e:
            print(e)
            return False, str(e), {}

    @staticmethod
    def _send_sendgrid_email(to_emails, subject, message, template_id, dynamic_data, cc_emails=None, bcc_emails=None, attachments=None):
        mail = Mail()
        mail.from_email = Email(os.getenv('SENDGRID_SENDER_EMAIL'))

        if template_id:
            mail.template_id = template_id
            for email in to_emails:
                personalization = Personalization()
                personalization.add_to(To(email))
                if dynamic_data:
                    for key, value in dynamic_data.items():
                        personalization.dynamic_template_data = {}
                        personalization.dynamic_template_data[key] = value
                if cc_emails:
                    for cc_email in cc_emails:
                        personalization.add_cc(Cc(cc_email))
                if bcc_emails:
                    for bcc_email in bcc_emails:
                        personalization.add_bcc(Bcc(bcc_email))
                mail.add_personalization(personalization)
        else:
            mail.subject = subject
            mail.content = Content("text/html", message if message else "")
            for email in to_emails:
                mail.add_to(To(email))
            if cc_emails:
                for cc_email in cc_emails:
                    mail.add_cc(Cc(cc_email))
            if bcc_emails:
                for bcc_email in bcc_emails:
                    mail.add_bcc(Bcc(bcc_email))
        
        if attachments:
            for attachment in attachments:
                attachment_obj = Attachment(
                    FileContent(attachment['file']),
                    FileName(attachment['file_name']),
                    FileType('application/octet-stream')
                )
                mail.add_attachment(attachment_obj)

        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(mail)
            return response.status_code, response.body, response.headers
        except Exception as e:
            print(str(e))
            return False, str(e), {}
