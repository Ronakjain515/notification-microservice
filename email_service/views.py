import copy
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailSerializer
from .backend import EmailService
from utilities.utils import ResponseInfo, CustomException
from utilities import messages
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from utilities.sqs import push_message_to_sqs
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
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        self.failed_messages_response_list = list()
        self.failed_payload = list()
        logger.info("Initializing SendEmailAPIView.")
        super(SendEmailAPIView, self).__init__(**kwargs)

    def send_email_service(self, service_type, payload):
        """
        Method to make service for push service.
        """
        return EmailService().send_email(service_type, **payload)

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

        use_sqs = request.data.get('use_sqs', False)
        # Serialize and validate the request data
        for requested_data in request.data.get('payload', []):
            serializer = self.get_serializer(data=requested_data, context={'provider_type': provider_type})
            if serializer.is_valid():
                # Extract validated data
                validated_data = serializer.validated_data

                # Log the email sending process
                logger.info(f"Sending email with data: {validated_data}")

                if use_sqs:
                    message = {
                        "provider_type": provider_type,
                        "service_type": "email",
                        "service_data": {
                            **validated_data
                        }
                    }
                    push_message_to_sqs(message)

                else:
                    # Call EmailService to send the email
                    response = self.send_email_service(provider_type, serializer.validated_data)
                    logger.info("Email sent successfully.")
                    success, body, headers = response

                    if success:
                        # Configure response for successful email sending
                        self.response_format["data"] = None
                        self.response_format["error"] = None
                        self.response_format["status_code"] = status.HTTP_200_OK
                        self.response_format["message"] = [messages.SEND_SUCCESS.format("Email")]
                    else:
                        # Configure response for failed email sending
                        payload_copy = copy.deepcopy(requested_data)
                        payload_copy["errors"] = body
                        self.failed_payload.append(payload_copy)                        
                        logger.error(f"Failed to send email. Error: {body}")
            else:

                payload_copy = copy.deepcopy(requested_data)
                payload_copy["errors"] = serializer.errors
                self.failed_payload.append(payload_copy)
                # Log validation errors
                logger.warning(f"Validation errors: {serializer.errors}")

        response_data = {
            "failed_payload": None
        }
        if len(self.failed_payload) > 0:
            response_data["failed_payload"] = self.failed_payload

        # Update the response format for success
        self.response_format["data"] = response_data
        self.response_format["error"] = None
        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["message"] = [messages.SEND_SUCCESS.format("Email")]
        return Response(self.response_format)
