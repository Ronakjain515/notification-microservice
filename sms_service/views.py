from rest_framework.generics import CreateAPIView

from .serializers import SmsServiceSerializer

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

    def send_twilio_sms(self, send_to, message):
        print(f"twilio creds = {os.getenv('TWILIO_ACCOUNT_SID')}, {os.getenv('TWILIO_AUTH_TOKEN')}")
        print(f"send_to = {send_to}, message = {message}")
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        message_sent = client.messages.create(
            body=message,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            to=send_to
        )
        print(f"message id {message_sent.sid}")


    def post(self, request, *args, **kwargs):
        print(f"request.data = {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print("is valid")
            send_to = request.data.get("send_to")
            medium = request.data.get("medium")
            service = request.data.get("service")
            if medium == "SMS" and service == "TWILIO":
                message = request.data.get("message")
                for ph_no in send_to:

                    self.send_twilio_sms(ph_no, message)
            else:
                self.response_format["message"] = ["Service coming soon."]
                self.response_format["status_code"] = status.HTTP_404_NOT_FOUND

        return Response(self.response_format, status=self.response_format["status_code"])
