from drf_yasg import openapi
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from utilities import messages
from .backend import PushService
from utilities.utils import (
    logger,
    ResponseInfo,
)
from .serializers import (
    SendFirebasePushSerializer,
)
from utilities.permissions import IsAuthenticatedPermission


class SendPushAPIView(CreateAPIView):
    """
    API view for sending push notifications.
    """
    permission_classes = (IsAuthenticatedPermission, )
    authentication_classes = ()
    serializer_class = SendFirebasePushSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for initializing response format.
        """
        self.response_format = ResponseInfo().response
        super(SendPushAPIView, self).__init__(**kwargs)
        logger.debug("SendPushAPIView instance initialized.")

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'service_type',
                openapi.IN_PATH,
                description="Service type (e.g., 'firebase')",
                type=openapi.TYPE_STRING,
                enum=['firebase']
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to send push notifications.
        """
        logger.info("POST request received for sending push notifications.")

        # Retrieve the service type from URL parameters
        service_type = kwargs.get("service_type")
        logger.debug(f"Service type received: {service_type}")

        # Serialize the incoming request data
        push_serializer = self.get_serializer(data=request.data)

        if push_serializer.is_valid(raise_exception=True):
            title = push_serializer.validated_data.get("title")
            content = push_serializer.validated_data.get("content")
            tokens = push_serializer.validated_data.get("tokens")
            extra_args = push_serializer.validated_data.get("extra_args")
            badge_count = push_serializer.validated_data.get("badge_count")

            logger.info("Push notification data validated successfully.")

            try:
                PushService().send_push(service_type, title, content, extra_args, tokens, badge_count)
                logger.info("Push notification sent successfully.")

                # Update the response format for success
                self.response_format["data"] = None
                self.response_format["error"] = None
                self.response_format["status_code"] = status.HTTP_200_OK
                self.response_format["message"] = [messages.SHARED.format("Push Notification")]
            except Exception as e:
                # Log any errors that occur during push notification sending
                logger.error(f"Error sending push notification: {str(e)}")
                self.response_format["data"] = None
                self.response_format["error"] = str(e)
                self.response_format["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
                self.response_format["message"] = [messages.FAILURE.format("Push Notification")]
                return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Log validation failures
            logger.warning("Push serializer validation failed.")

        return Response(self.response_format)
