from django.urls import path

from .views import SmsServiceAPIView

urlpatterns = [
    path("sms_service/send", SmsServiceAPIView.as_view(), name="send-sms"),
]


