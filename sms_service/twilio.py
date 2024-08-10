import os
from twilio.rest import Client

from utilities.utils import logger


def send_twilio_sms(message, send_to):
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    message_sent = client.messages.create(
        body=message,
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        to=send_to
    )
    if message.sid:
        message_response = client.messages(message.sid).fetch()
        if message_response.status == 200:
            logger.info(f"sms sent to {send_to} message sid - {message_sent.sid}")
        else:
            logger.info(f"failed to send sms to {send_to} message sid - {message_sent.sid}")
    else:
        logger.info(f"failed to send sms to {send_to} message sid - {message_sent.sid}")

