from .twilio import send_twilio_sms


class SmsService:
    @staticmethod
    def send_sms(service, message, send_to):

        if service == "twilio":
            for ph_no in send_to:
                send_twilio_sms(message, ph_no)
        else:
            return None

