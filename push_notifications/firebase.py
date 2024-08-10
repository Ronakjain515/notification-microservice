import os
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

from utilities.utils import CustomException


try:
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
    firebase_admin.initialize_app(cred)
except ValueError:
    pass


def send_firebase_push_notification(request_data, tokens, badge_count):
    """
    Method to send push notification to users.
    """
    try:
        firebase_admin.get_app()
    except ValueError as e:
        raise CustomException("firebase is not initialized.")

    response = messaging.MulticastMessage(
        data=request_data,
        tokens=list(set(tokens)),
        notification=messaging.Notification(
            title=request_data["title"],
            body=request_data["content_in_notification"]
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(badge=badge_count, sound="default"),
            ),
        ),
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority='high',
            notification=messaging.AndroidNotification(
                channel_id="HealthLink-Notifications"
            ),
        ),
        webpush=messaging.WebpushConfig(
            fcm_options=messaging.WebpushFCMOptions(
                link="https://meet.google.com/npf-fiiy-ggr?authuser=0"
            )
        )
    )
    messaging.send_multicast(response)
    return response
