import json

from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework import serializers
from rest_framework.response import Response

from utilities.utils import (
    ResponseInfo,
)
from utilities import messages
from utilities.permissions import (
    IsAuthenticatedPermission,
)
from utilities.sqs import receiver_message_sqs
from push_notifications.views import SendPushAPIView
from email_service.views import SendEmailAPIView
from sms_service.views import SmsServiceAPIView


class GetSQSDataAPIView(CreateAPIView):
    """
    Class for creating api for getting data for scheduler.
    """

    permission_classes = (IsAuthenticatedPermission,)
    authentication_classes = ()
    serializer_class = serializers.Serializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        self.pagination = None
        super(GetSQSDataAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        POSt Method to get data from SQS.
        """
        print("Data HERE", request.data)
        request_data = json.loads(request.data["json_string"])
        receipt_handle = request.data["receipt_handle"]

        if request_data["service_type"] == "push":
            SendPushAPIView().send_push_service(request_data["provider_type"], request_data["service_data"])
            receiver_message_sqs(receipt_handle)

        if request_data["service_type"] == "sms":
            SmsServiceAPIView().send_sms_service(request_data["provider_type"], request_data["service_data"])
            receiver_message_sqs(receipt_handle)

        if request_data["service_type"] == "email":
            SendEmailAPIView().send_email_service(request_data["provider_type"], request_data["service_data"])
            receiver_message_sqs(receipt_handle)

        self.response_format["data"] = None
        self.response_format["error"] = None
        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["message"] = [messages.SUCCESS]
        return Response(self.response_format)
