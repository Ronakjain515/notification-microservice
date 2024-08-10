import os
from twilio.rest import Client
from twilio.base.client_base import TwilioException

from utilities.utils import logger, CustomException


def send_twilio_sms(message, send_to):
    failed_messages = list()
    try:
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        message_sent = client.messages.create(
            body=message,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            to=send_to
        )
        logger.info(f"SMS sent to {send_to}, SID: {message_sent.sid}")

    except TwilioException as e:
        logger.error(f"Failed to send SMS to {send_to}. Error: {str(e)}")
        if type(e) == TwilioException and str(e) == "Credentials are required to create a TwilioClient":
            logger.error("Invalid Twilio credentials.")
            raise CustomException("Invalid Twilio credentials.")
        elif e.status == 400:
            return send_to
    #
    # return failed_messages


