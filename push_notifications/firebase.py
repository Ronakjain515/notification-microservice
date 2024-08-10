import os
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

from utilities.utils import (
    logger,
    CustomException,
)


try:
    # Load Firebase credentials from environment variables
    cred = credentials.Certificate({
        "type": os.getenv("FIREBASE_TYPE"),
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
        "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
        "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN")
    })
    # Initialize the Firebase app with the credentials
    firebase_admin.initialize_app(cred)
except ValueError:
    pass


def send_firebase_push_notification(title, content, extra_args, tokens, badge_count):
    """
    Sends a push notification to users via Firebase.

    :param title: The title of the push notification.
    :param content: The body content of the push notification.
    :param extra_args: Additional data to send with the notification.
    :param tokens: List of device tokens to send the notification to.
    :param badge_count: Badge count to display on the app icon.
    :return: The response from Firebase after sending the notification.
    :raises CustomException: If Firebase is not initialized or an error occurs during sending.
    """
    logger.info("Preparing to send push notification via Firebase.")

    # Check if Firebase is initialized
    try:
        firebase_admin.get_app()
        logger.info("Firebase is initialized.")
    except ValueError as e:
        logger.error("Firebase is not initialized.")
        raise CustomException("Firebase is not initialized.")

    # Create the multicast message for Firebase
    try:
        response = messaging.MulticastMessage(
            data=extra_args,
            tokens=list(set(tokens)),  # Remove duplicate tokens
            notification=messaging.Notification(
                title=title,
                body=content
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(badge=badge_count, sound="default"),
                ),
            ),
            android=messaging.AndroidConfig(
                ttl=datetime.timedelta(seconds=3600),  # Time-to-live
                priority='high',
                notification=messaging.AndroidNotification(
                    channel_id="Notification-Microservice"
                ),
            ),
            webpush=messaging.WebpushConfig(
                fcm_options=messaging.WebpushFCMOptions(
                    link="https://google.com"
                )
            )
        )

        # Send the multicast message
        result = messaging.send_multicast(response)
        logger.info("Push notification sent successfully.")
        logger.debug(f"Response: {result}")

        return result
    except Exception as e:
        logger.error(f"Failed to send push notification: {str(e)}")
        raise CustomException(f"Failed to send push notification: {str(e)}")
