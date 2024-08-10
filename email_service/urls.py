from django.urls import path
from .views import SendEmailAPIView
from .path_converter import EmailTypeConverter

urlpatterns = [
    path('send/<emailtype:email_type>/', SendEmailAPIView.as_view(), name='send-email'),
]
