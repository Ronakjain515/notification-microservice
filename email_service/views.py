from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailSerializer
from .backend import EmailService
from utilities.utils import ResponseInfo, CustomException
from utilities import messages
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from utilities.utils import logger
from utilities.permissions import IsAuthenticatedPermission

class SendEmailAPIView(CreateAPIView):
    """
    send email using sendgrid and smtp service
    """
    # Set custom permissions and authentication for this view
    permission_classes = (IsAuthenticatedPermission, )
    authentication_classes = ()
    
    # Specify the serializer class for this view
    serializer_class = EmailSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for setting up the response format for this view.
        """
        # Initialize response format from ResponseInfo utility
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
        """
        Handle POST requests to send an email. Validates the request and calls the EmailService to send the email.
        """
        EMAIL_CHOICES = ['sendgrid', 'smtp']

        # Log the received provider type
        logger.debug(f"Received request with provider_type: {provider_type}")

        # Validate provider_type
        if provider_type not in EMAIL_CHOICES:
            error_message = messages.VALID_PARAMS.format(', '.join(EMAIL_CHOICES))
            logger.error(f"Invalid provider_type: {provider_type}. Error: {error_message}")
            raise CustomException(error_message)

        # Serialize and validate the request data
        serializer = self.get_serializer(data=request.data, context={'provider_type': provider_type})
        if serializer.is_valid():
            # Extract validated data
            validated_data = serializer.validated_data
            to_emails = validated_data.get('to')
            cc_emails = validated_data.get('cc')
            bcc_emails = validated_data.get('bcc')
            subject = validated_data.get('subject')
            message = validated_data.get('message')
            template_id = validated_data.get('template_id')
            dynamic_data = validated_data.get('dynamic_template_data')
            attachments = validated_data.get('attachments')

            # Log the email sending process
            logger.info(f"Sending email with data: {validated_data}")

            # Call EmailService to send the email
            response = EmailService.send_email(to_emails, subject, message, template_id, dynamic_data, provider_type, cc_emails, bcc_emails, attachments)
            success, body, headers = response

            if success:
                # Configure response for successful email sending
                self.response_format["data"] = None
                self.response_format["error"] = None
                self.response_format["status_code"] = status.HTTP_200_OK
                self.response_format["message"] = [messages.SEND_SUCCESS.format("Email")]

                logger.info("Email sent successfully.")
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                # Configure response for failed email sending
                self.response_format["data"] = None
                self.response_format["error"] = messages.FAILURE
                self.response_format["status_code"] = status.HTTP_200_OK
                self.response_format["message"] = [body]

                logger.error(f"Failed to send email. Error: {body}")
                return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Log validation errors
            logger.warning(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
