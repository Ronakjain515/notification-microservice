from django.urls import path

from .views import SmsServiceAPIView


urlpatterns = [
    path("send/sms/<str:service_type>/", SmsServiceAPIView.as_view(), name="send-sms"),
]

