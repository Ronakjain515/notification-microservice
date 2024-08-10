import copy
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
    CustomException,
)
from .serializers import (
    SendFirebasePushSerializer,
)
from utilities.sqs import push_message_to_sqs
from utilities.constants import PUSH_SERVICE_CHOICE
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
        self.failed_messages_response_list = list()
        self.failed_payload = list()
        super(SendPushAPIView, self).__init__(**kwargs)
        logger.debug("SendPushAPIView instance initialized.")

    def send_push_service(self, service_type, payload):
        """
        Method to make service for push service.
        """
        PushService().send_push(service_type, payload)

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
        service_type = self.kwargs["service_type"]
        logger.debug(f"Service type received: {service_type}")

        if service_type not in PUSH_SERVICE_CHOICE:
            logger.error(f"Invalid service type: {service_type}")
            raise CustomException("Invalid service type.", 400)

        use_sqs = request.data.get("use_sqs", False)

        logger.debug(f"Looping for payload.")
        for request_data in request.data.get("payload", []):
            # Serialize the incoming request data
            push_serializer = self.get_serializer(data=request_data)

            if push_serializer.is_valid(raise_exception=False):

                logger.info("Push notification data validated successfully.")

                try:
                    if use_sqs:
                        message = {
                            "provider_type": "firebase",
                            "service_type": "push",
                            "service_data": push_serializer.validated_data
                        }
                        push_message_to_sqs(message)
                    else:
                        self.send_push_service(service_type, push_serializer.validated_data)
                        logger.info("Push notification sent successfully.")

                except Exception as e:
                    # Log any errors that occur during push notification sending
                    logger.error(f"Error sending push notification: {str(e)}")
                    self.response_format["data"] = None
                    self.response_format["error"] = str(e)
                    self.response_format["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
                    self.response_format["message"] = [messages.FAILURE.format("Push Notification")]
                    return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                payload_copy = copy.deepcopy(request_data)
                payload_copy["errors"] = push_serializer.errors
                self.failed_payload.append(payload_copy)

        response_data = {
            "failed_payload": None
        }
        if len(self.failed_payload) > 0:
            response_data["failed_payload"] = self.failed_payload

        # Update the response format for success
        self.response_format["data"] = response_data
        self.response_format["error"] = None
        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["message"] = [messages.SHARED.format("Push Notification")]
        return Response(self.response_format)
