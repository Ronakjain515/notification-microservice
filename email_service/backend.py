from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Personalization
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

class EmailService:
    @staticmethod
    def send_email(to_emails, subject=None, message=None, template_id=None, dynamic_data=None, email_type=None):
        if not isinstance(to_emails, list):
            to_emails = [to_emails]

        if email_type == 'smtp':
            return EmailService._send_smtp_email(to_emails, subject, message)
        elif email_type == 'sendgrid':
            return EmailService._send_sendgrid_email(to_emails, subject, message, template_id, dynamic_data)
        else:
            raise ValueError("Invalid email_type. Expected 'smtp' or 'sendgrid'.")

    @staticmethod
    def _send_smtp_email(to_emails, subject, message):
        try:
            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, to_emails)
            email.content_subtype = "html"  # Main content is now text/html
            email.send()
            return 200, "Email sent successfully via SMTP", {}
        except Exception as e:
            print(e)
            return 500, str(e), {}

    @staticmethod
    def _send_sendgrid_email(to_emails, subject, message, template_id, dynamic_data):
        mail = Mail()
        mail.from_email = Email(settings.SENDGRID_SENDER_EMAIL)

        if template_id:
            mail.template_id = template_id
            for email in to_emails:
                personalization = Personalization()
                personalization.add_to(To(email))
                for key, value in dynamic_data.items():
                    personalization.dynamic_template_data[key] = value
                mail.add_personalization(personalization)
        else:
            mail.subject = subject
            mail.html_content = message if message else ""
            for email in to_emails:
                mail.add_to(To(email))

        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(mail)
            return response.ok, response.body, response.headers
        except Exception as e:
            print(e)
            return 500, str(e), {}
