from rest_framework import serializers

from utilities.constants import (
    MEDIUM_CHOICE,
    SMS_SERVICE_CHOICE,
)


class SendPushSerializer(serializers.Serializer):
    """
    Serializer class for sending push notifications.
    """
    medium = serializers.ChoiceField(choices=MEDIUM_CHOICE, allow_null=False, allow_blank=False)
    service = serializers.ChoiceField(choices=SMS_SERVICE_CHOICE, allow_null=False, allow_blank=False)
