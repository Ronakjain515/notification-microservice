from django.urls import path

from .views import (
    SendPushAPIView,
)


urlpatterns = [
    path("send/push/<str:service_type>/", SendPushAPIView.as_view(), name="send-push"),
]
