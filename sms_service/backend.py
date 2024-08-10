from .twilio import send_twilio_sms
from utilities.utils import logger


class SmsService:
    @staticmethod
    def send_sms(service, message, send_to):

        if service == "twilio":
            failed_message_list = list()
            for ph_no in send_to:
                failed_message = send_twilio_sms(message, ph_no)
                if failed_message:
                    failed_message_list.append(failed_message)
            return failed_message_list
        else:
            logger.warning(f"Unsupported service: {service}")
            return None

