MEDIUM_CHOICE = (
    ("SMS", "Sms"),
    ("EMAIL", "Email"),
    ("PUSH", "Push")
)

SMS_SERVICE_CHOICE = (
    ("TWILIO", "Twilio"),
    ("SNS", "Sns")
)


class SmsServiceSerializer(serializers.Serializer):
    medium = serializers.ChoiceField(choices=MEDIUM_CHOICE, allow_null=False, allow_blank=False)
    service = serializers.ChoiceField(choices=SMS_SERVICE_CHOICE, allow_null=False, allow_blank=False)
    message = serializers.CharField(allow_null=False, allow_blank=False)
    send_to = serializers.ListField(child=serializers.CharField(allow_null=False, allow_blank=False), allow_null=False, allow_empty=False)