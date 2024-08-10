from rest_framework import serializers


class SendFirebasePushSerializer(serializers.Serializer):
    """
    Serializer class for sending push notifications.
    """
    title = serializers.CharField(allow_null=False, required=True, allow_blank=False)
    content = serializers.CharField(allow_null=False, required=True, allow_blank=False)
    tokens = serializers.ListField(allow_null=False, required=True, allow_empty=False)
    badge_count = serializers.IntegerField(allow_null=True, required=False)
    extra_args = serializers.JSONField(allow_null=True, required=False)
