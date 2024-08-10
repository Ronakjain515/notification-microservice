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
        request_data = request.data["json_string"]

        # if request_data["service"] == "push":
        #     pass
        #
        # if request_data["service"] == "sms":
        #     pass
        #
        # if request_data["service"] == "email":
        #     pass

        self.response_format["data"] = None
        self.response_format["error"] = None
        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["message"] = [messages.SUCCESS]
        return Response(self.response_format)
