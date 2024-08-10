from rest_framework import serializers

from utilities.constants import (
    MEDIUM_CHOICE,
    SMS_SERVICE_CHOICE
)


class SmsServiceSerializer(serializers.Serializer):
    use_sqs = serializers.BooleanField(allow_null=False, allow_blank=False)
    message = serializers.CharField(allow_null=False, allow_blank=False)
    send_to = serializers.ListField(child=serializers.CharField(allow_null=False, allow_blank=False), allow_null=False, allow_empty=False)