# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailSerializer
from .backend import EmailService

class SendEmailAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email_type = kwargs.get('email_type')
        
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            to_emails = validated_data.get('to_emails')
            subject = validated_data.get('subject')
            message = validated_data.get('message')
            template_id = validated_data.get('template_id')
            dynamic_data = validated_data.get('dynamic_data', {})

            response = EmailService.send_email(to_emails, subject, message, template_id, dynamic_data, email_type)
            success, body, headers = response

            if success:
                return Response({'status': 'Email sent successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': body}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
