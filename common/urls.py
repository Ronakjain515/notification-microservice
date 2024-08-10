from django.urls import path
from .views import GetSQSDataAPIView


urlpatterns = [
    path('getSQSData', GetSQSDataAPIView.as_view(), name='get-sqs-data'),
]
