# serializers.py
from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    to_emails = serializers.ListField(
        child=serializers.EmailField(), 
        allow_empty=False
    )
    subject = serializers.CharField(required=False)
    message = serializers.CharField(required=False)
    template_id = serializers.CharField(required=False)
    dynamic_data = serializers.DictField(required=False, allow_null=True, default=dict)

    def validate(self, data):
        if not data.get('template_id'):
            # Ensure that both subject and message are provided for plain emails
            if not data.get('subject') or not data.get('message'):
                raise serializers.ValidationError({
                    'subject': 'Subject is required for plain messages',
                    'message': 'Message is required for plain messages'
                })
        return data
