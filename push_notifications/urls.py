from django.urls import path

from .views import (
    SendPushAPIView,
)


urlpatterns = [
    path("send", SendPushAPIView.as_view(), name="send-push"),
]
