from django.urls import path
from .views import SendEmailAPIView

urlpatterns = [
    path('send/email/<str:provider_type>/', SendEmailAPIView.as_view(), name='send-email'),
]
