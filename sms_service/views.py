from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from utilities.utils import (
    ResponseInfo,
    CustomException)
from .serializers import SmsServiceSerializer
from utilities.constants import SMS_SERVICE_CHOICE
from .backend import SmsService


class SmsServiceAPIView(CreateAPIView):
    """
    Class to create api to send sms to phone numbers.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = SmsServiceSerializer

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(SmsServiceAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        service_type = self.kwargs["service_type"]
        if service_type not in SMS_SERVICE_CHOICE:
            raise CustomException("Invalid service type.", 400)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            send_to = serializer.validated_data.get("send_to")
            message = serializer.validated_data.get("message")
            SmsService().send_sms(service_type, message, send_to)

        return Response(self.response_format, status=self.response_format["status_code"])
