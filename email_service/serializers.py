from rest_framework import serializers

class AttachmentSerializer(serializers.Serializer):
    """
    Serializer for handling file attachments in an email.
    
    Fields:
    - file_name: The name of the file attachment.
    - file: The base64-encoded content of the file.
    """
    file_name = serializers.CharField(max_length=255)
    file = serializers.CharField(allow_blank=True, allow_null=True)

class EmailSerializer(serializers.Serializer):
    """
    Serializer for validating email data input.
    
    Fields:
    - to: List of recipient email addresses.
    - subject: Subject of the email.
    - message: Body of the email.
    - template_id: (Optional) Template ID for templated emails.
    - dynamic_template_data: (Optional) Dictionary containing dynamic data for the email template.
    - cc: (Optional) List of CC email addresses.
    - bcc: (Optional) List of BCC email addresses.
    - attachments: (Optional) List of attachments.
    """
    to = serializers.ListField(
        child=serializers.EmailField(),
        allow_empty=False
    )
    subject = serializers.CharField(required=False)
    message = serializers.CharField(required=False)
    template_id = serializers.CharField(required=False)
    dynamic_template_data = serializers.DictField(required=False, allow_null=True, default=dict)
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
        child=AttachmentSerializer(),  # List of attachment dictionaries
        required=False,
        allow_empty=True
    )

    def validate(self, data):
        """
        Custom validation logic for the email data based on the provider type.
        
        - Ensures that the subject and message fields are provided if the provider type is 'smtp'.
        - Ensures that subject and message are provided if template_id is not specified.
        
        Parameters:
        - data: The input data to validate.
        
        Returns:
        - Validated data if no validation errors occur.
        
        Raises:
        - serializers.ValidationError: If validation checks fail.
        """
        # Validate based on provider type
        if self.context['provider_type'] == 'smtp':
            # For 'smtp', subject and message are required
            if not data.get('subject') or not data.get('message'):
                raise serializers.ValidationError({
                    'subject': 'Subject is required for email',
                    'message': 'Message is required for email'
                })

        # If no template_id is provided, ensure that subject and message are both provided
        if not data.get('template_id'):
            if not data.get('subject') or not data.get('message'):
                raise serializers.ValidationError({
                    'subject': 'Subject is required for email',
                    'message': 'Message is required for email'
                })

        return data
