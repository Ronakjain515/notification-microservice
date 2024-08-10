from django.urls import path
from .views import SendEmailAPIView

urlpatterns = [
    path('send/<str:email_type>/', SendEmailAPIView.as_view(), name='send-email'),
]
