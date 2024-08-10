from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from utilities.utils import (
    logger,
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
            logger.error(f"Invalid service type: {service_type}")
            raise CustomException("Invalid service type.", 400)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            send_to = serializer.validated_data.get("send_to")
            message = serializer.validated_data.get("message")
            failed_message = SmsService().send_sms(service_type, message, send_to)

            if len(failed_message) > 0:
                logger.warning(f"Partial success. Failed to send SMS to: {failed_message}")
                self.response_format["data"] = failed_message
                self.response_format["status_code"] = status.HTTP_207_MULTI_STATUS
                self.response_format["error"] = "Failed Messages."
                self.response_format["message"] = "Partial Success."
            else:
                logger.info(f"SMS sent successfully to all recipients: {send_to}")

        return Response(self.response_format, status=self.response_format["status_code"])
