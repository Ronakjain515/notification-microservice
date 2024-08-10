from utilities.utils import CustomException, logger
from .firebase import send_firebase_push_notification


class PushService:
    @staticmethod
    def send_push(service, title, content, extra_args, tokens, badge_count):
        """
        Method to send push notifications based on the specified service type.

        :param service: The service type to use for sending the push notification (e.g., 'firebase', 'sns').
        :param title: The title of the push notification.
        :param content: The content of the push notification.
        :param extra_args: Additional arguments for the push notification.
        :param tokens: A list of device tokens to send the push notification to.
        :param badge_count: Badge count to display on the app icon.
        :raises CustomException: If the service type is not recognized.
        """
        logger.info("Attempting to send push notification.")
        logger.debug(f"Service: {service}")
        logger.debug(f"Title: {title}")
        logger.debug(f"Content: {content}")
        logger.debug(f"Extra args: {extra_args}")
        logger.debug(f"Tokens: {tokens}")
        logger.debug(f"Badge count: {badge_count}")

        if service == "firebase":
            logger.info("Sending push notification via Firebase.")
            try:
                send_firebase_push_notification(title, content, extra_args, tokens, badge_count)
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
