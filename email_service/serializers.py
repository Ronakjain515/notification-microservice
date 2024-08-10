from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    to = serializers.ListField(
        child=serializers.EmailField(),
        allow_empty=False
    )
    subject = serializers.CharField(required=False)
    message = serializers.CharField(required=False)
    template_id = serializers.CharField(required=False)
    dynamic_data = serializers.DictField(required=False, allow_null=True, default=dict)
    cc = serializers.ListField(
        child=serializers.EmailField(),
        required=False,
        allow_empty=True
    )
    bcc = serializers.ListField(
        child=serializers.EmailField(),
        required=False,
        allow_empty=True
    )
    attachments = serializers.ListField(
        child=serializers.DictField(required=False, allow_null=True, default=dict),
        required=False,
        allow_empty=True
    )

    def validate(self, data):
        if not data.get('template_id'):
            # Ensure that both subject and message are provided for plain emails
            if not data.get('subject') or not data.get('message'):
                raise serializers.ValidationError({
                    'subject': 'Subject is required for plain messages',
                    'message': 'Message is required for plain messages'
                })
        return data
