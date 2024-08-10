# views.py
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailSerializer
from .backend import EmailService
from utilities.utils import ResponseInfo, CustomException
from utilities import messages
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class SendEmailAPIView(CreateAPIView):
    serializer_class = EmailSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(SendEmailAPIView, self).__init__(**kwargs)

    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter(
                    'provider_type',
                    openapi.IN_PATH,
                    description="Provider type",
                    type=openapi.TYPE_STRING,
                    enum=['smtp', 'sendgrid']
                ),
            ]
        )
    def post(self, request, provider_type, *args, **kwargs):
        EMAIL_CHOICES = ['sendgrid', 'smtp']

        if provider_type not in EMAIL_CHOICES:
            raise CustomException(messages.VALID_PARAMS.format(', '.join(EMAIL_CHOICES)))

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            to_emails = validated_data.get('to')
            cc_emails = validated_data.get('cc')
            bcc_emails = validated_data.get('bcc')
            subject = validated_data.get('subject')
            message = validated_data.get('message')
            template_id = validated_data.get('template_id')
            dynamic_data = validated_data.get('dynamic_template_data')
            attachments = validated_data.get('attachments')

            response = EmailService.send_email(to_emails, subject, message, template_id, dynamic_data, provider_type, cc_emails, bcc_emails, attachments)
            success, body, headers = response

            if success:
                self.response_format["data"] = None
                self.response_format["error"] = None
                self.response_format["status_code"] = status.HTTP_200_OK
                self.response_format["message"] = [messages.SEND_SUCCESS.format("Email")]

                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format["data"] = None
                self.response_format["error"] = messages.FAILURE
                self.response_format["status_code"] = status.HTTP_200_OK
                self.response_format["message"] = [messages.SEND_FAILED.format("email")]

                return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
