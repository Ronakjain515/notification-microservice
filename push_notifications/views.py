from drf_yasg import openapi
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from utilities import messages
from .backend import PushService
from utilities.utils import ResponseInfo
from .serializers import (
    SendFirebasePushSerializer,
)


class SendPushAPIView(CreateAPIView):
    """
    Class to create api for sending push notifications.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = SendFirebasePushSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(SendPushAPIView, self).__init__(**kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'service_type',
                openapi.IN_PATH,
                description="Service type",
                type=openapi.TYPE_STRING,
                enum=['firebase']
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        """
        POST Method for Send push notifications.
        """
        # service type key.
        service_type = kwargs.get("service_type")

        push_serializer = self.get_serializer(data=request.data)

        if push_serializer.is_valid(raise_exception=True):

            title = push_serializer.validated_data.get("title")
            content = push_serializer.validated_data.get("content")
            tokens = push_serializer.validated_data.get("tokens")
            extra_args = push_serializer.validated_data.get("extra_args")
            badge_count = push_serializer.validated_data.get("badge_count")
            PushService().send_push(service_type, title, content, extra_args, tokens, badge_count)

            self.response_format["data"] = None
            self.response_format["error"] = None
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["message"] = [messages.SHARED.format("Push Notification")]
        return Response(self.response_format)
