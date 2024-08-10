# path_converters.py
from django.urls import register_converter

class EmailTypeConverter:
    regex = 'sendgrid|smtp'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value

# Register the converter
register_converter(EmailTypeConverter, 'emailtype')
