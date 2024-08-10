from utilities.utils import CustomException
from .firebase import send_firebase_push_notification


class PushService:
    @staticmethod
    def send_push(service, title, content, extra_args, tokens, badge_count):
        """
        Method to send push notifications.
        """
        if service == "firebase":
            send_firebase_push_notification(title, content, extra_args, tokens, badge_count)

        elif service == "sns":
            pass
        else:
            raise CustomException("service type is required.")
