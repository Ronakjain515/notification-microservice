from .sendgrid import send_sendgrid_email
from .smtp import send_smtp_email
from utilities.utils import logger

class EmailService:
    @staticmethod
    def send_email(provider_type, to, subject=None, message=None, template_id=None, dynamic_template_data=None, cc=None, bcc=None, attachments=None):
        """
        Sends an email using the specified provider (SMTP or SendGrid).
        
        Parameters:
        - provider_type: The email provider to use ('smtp' or 'sendgrid').
        - to: List of recipient email addresses.
        - subject: Subject of the email.
        - message: Body of the email.
        - template_id: (Optional) ID of the email template for SendGrid.
        - dynamic_template_data: (Optional) Data to populate dynamic fields in the email template.
        - cc: (Optional) List of CC email addresses.
        - bcc: (Optional) List of BCC email addresses.
        - attachments: (Optional) List of file attachments to include in the email.
        
        Returns:
        A tuple (success, response_body, headers) where:
        - success: Boolean indicating if the email was sent successfully.
        - response_body: Message or error description.
        - headers: Any additional headers returned by the email service.
        """
        try:
            # Ensure lists are used for email addresses and attachments
            if not isinstance(to, list):
                to = [to]
            if cc and not isinstance(cc, list):
                cc = [cc]
            if bcc and not isinstance(bcc, list):
                bcc = [bcc]
            if attachments and not isinstance(attachments, list):
                attachments = [attachments]

            # Log email sending details
            logger.info(f"Sending email. Provider: {provider_type}, To: {to}, Subject: {subject}")

            # Call the appropriate method based on the provider_type
            if provider_type == 'smtp':
                response = EmailService._send_smtp_email(to, subject, message, cc, bcc, attachments)
                logger.info("SMTP email sent successfully.")
                return response
            elif provider_type == 'sendgrid':
                response = EmailService._send_sendgrid_email(to, subject, message, template_id, dynamic_template_data, cc, bcc, attachments)
                logger.info("SendGrid email sent successfully.")
                return response
            else:
                # Handle invalid provider_type
                raise ValueError("Invalid provider_type. Expected 'smtp' or 'sendgrid'.")
        except Exception as e:
            # Log any errors that occur
            logger.error(f"Error in sending email: {e}")
            return False, str(e), {}

    @staticmethod
    def _send_smtp_email(to_emails, subject, message, cc_emails=None, bcc_emails=None, attachments=None):
        """
        Sends an email using the SMTP provider.
        
        Parameters:
        - to_emails: List of recipient email addresses.
        - subject: Subject of the email.
        - message: Body of the email.
        - cc_emails: (Optional) List of CC email addresses.
        - bcc_emails: (Optional) List of BCC email addresses.
        - attachments: (Optional) List of file attachments to include in the email.
        
        Returns:
        A tuple (success, response_body, headers) where:
        - success: Boolean indicating if the email was sent successfully.
        - response_body: Message or error description.
        - headers: Any additional headers returned by the email service.
        """
        try:
            # Log preparation details for SMTP email
            logger.debug(f"Preparing to send SMTP email. To: {to_emails}, Subject: {subject}")
            # Call the actual SMTP email sending function
            response = send_smtp_email(to_emails, subject, message, cc_emails, bcc_emails, attachments)
            # Log the response from SMTP email sending
            logger.debug(f"SMTP email response: {response}")
            return response
        except Exception as e:
            # Log any errors that occur during SMTP email sending
            logger.error(f"Error sending SMTP email: {e}")
            return False, str(e), {}

    @staticmethod
    def _send_sendgrid_email(to_emails, subject, message, template_id, dynamic_data, cc_emails=None, bcc_emails=None, attachments=None):
        """
        Sends an email using the SendGrid provider.
        
        Parameters:
        - to_emails: List of recipient email addresses.
        - subject: Subject of the email.
        - message: Body of the email.
        - template_id: (Optional) ID of the email template for SendGrid.
        - dynamic_data: (Optional) Data to populate dynamic fields in the email template.
        - cc_emails: (Optional) List of CC email addresses.
        - bcc_emails: (Optional) List of BCC email addresses.
        - attachments: (Optional) List of file attachments to include in the email.
        
        Returns:
        A tuple (success, response_body, headers) where:
        - success: Boolean indicating if the email was sent successfully.
        - response_body: Message or error description.
        - headers: Any additional headers returned by the email service.
        """
        try:
            # Log preparation details for SendGrid email
            logger.debug(f"Preparing to send SendGrid email. To: {to_emails}, Subject: {subject}, Template ID: {template_id}")
            # Call the actual SendGrid email sending function
            response = send_sendgrid_email(to_emails, subject, message, template_id, dynamic_data, cc_emails, bcc_emails, attachments)
            # Log the response from SendGrid email sending
            logger.debug(f"SendGrid email response: {response}")
            return response
        except Exception as e:
            # Log any errors that occur during SendGrid email sending
            logger.error(f"Error sending SendGrid email: {e}")
            return False, str(e), {}
