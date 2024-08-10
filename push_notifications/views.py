from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework.response import Response

from utilities import messages
from .backend import PushService
from utilities.utils import ResponseInfo
from .serializers import SendPushSerializer


class SendPushAPIView(CreateAPIView):
    """
    Class to create api for sending push notifications.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = SendPushSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(SendPushAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        POST Method for Send push notifications.
        """
        PushService().send_push()
        self.response_format["data"] = None
        self.response_format["error"] = None
        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["message"] = [messages.SHARED.format("Push Notification")]
        return Response(self.response_format)
