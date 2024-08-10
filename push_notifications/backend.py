from .firebase import send_firebase_push_notification


class PushService:
    @staticmethod
    def send_push():
        """
        Method to send push notifications.
        """
        send_firebase_push_notification("request_data", "tokens", "badge_count")
