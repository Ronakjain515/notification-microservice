from utilities.utils import CustomException, logger
from .firebase import send_firebase_push_notification


class PushService:
    @staticmethod
    def send_push(service, payload):
        """
        Method to send push notifications based on the specified service type.

        :param service: The service type to use for sending the push notification (e.g., 'firebase', 'sns').
        :param payload: The payload is to use for request data to initiate push notification.
        :raises CustomException: If the service type is not recognized.
        """
        logger.info("Attempting to send push notification.")
        logger.debug(f"Service: {service}")
        logger.debug(f"Payload: {payload}")

        if service == "firebase":
            logger.info("Sending push notification via Firebase.")
            try:
                send_firebase_push_notification(payload["title"], payload["content"], payload["extra_args"], payload["tokens"], payload["badge_count"])
                logger.info("Push notification sent successfully via Firebase.")
            except Exception as e:
                logger.error(f"Failed to send push notification via Firebase: {str(e)}")
                raise

        elif service == "sns":
            logger.info("SNS service is not implemented.")
            # Implement SNS push notification logic.
            pass

        else:
            error_message = f"Unrecognized service type: {service}"
            logger.error(error_message)
            raise CustomException(error_message)
