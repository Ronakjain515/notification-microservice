# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailSerializer
from .backend import EmailService
from utilities.utils import ResponseInfo
from utilities import messages

class SendEmailAPIView(APIView):

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(SendEmailAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        email_type = kwargs.get('email_type')
        
        EMAIL_CHOICES = ['sendgrid', 'smtp']

        if email_type not in EMAIL_CHOICES:
            self.response_format["data"] = None
            self.response_format["error"] = messages.FAILURE
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = [messages.VALID_PARAMS.format(', '.join(EMAIL_CHOICES))]
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            to_emails = validated_data.get('to')
            cc_emails = validated_data.get('cc')
            bcc_emails = validated_data.get('bcc')
            subject = validated_data.get('subject')
            message = validated_data.get('message')
            template_id = validated_data.get('template_id')
            dynamic_data = validated_data.get('dynamic_data', {})
            attachments = validated_data.get('attachments')

            response = EmailService.send_email(to_emails, subject, message, template_id, dynamic_data, email_type, cc_emails, bcc_emails, attachments)
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
