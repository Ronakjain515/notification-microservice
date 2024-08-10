from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch


class SendPushAPIViewTestCase(APITestCase):
    """
    Test case for the SendPushAPIView.
    """

    def setUp(self):
        """
        Set up any initial data for the test case.
        """
        self.url = lambda service_type: reverse('send-push', kwargs={'service_type': service_type})
        self.valid_payload = {
            'title': 'Test Notification',
            'content': 'This is a test notification.',
            'tokens': ['token1', 'token2'],
            'extra_args': {'key': 'value'},
            'badge_count': 1
        }
        self.invalid_payload = {
            'title': '',  # Invalid payload: title is empty
            'content': 'This is a test notification.',
            'tokens': ['token1', 'token2'],
            'extra_args': {'key': 'value'},
            'badge_count': 1
        }

    @patch('your_app.views.PushService.send_push')
    def test_send_push_success(self, mock_send_push):
        """
        Test sending a push notification successfully.
        """
        mock_send_push.return_value = None  # Mock the PushService.send_push method

        response = self.client.post(self.url('firebase'), self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status_code'], status.HTTP_200_OK)
        self.assertIsNone(response.data['data'])
        self.assertIsNone(response.data['error'])
        self.assertEqual(response.data['message'], ['Push Notification shared successfully.'])

    @patch('your_app.views.PushService.send_push')
    def test_send_push_failure(self, mock_send_push):
        """
        Test failure in sending a push notification.
        """
        mock_send_push.side_effect = Exception("Test Exception")  # Simulate an exception

        response = self.client.post(self.url('firebase'), self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['status_code'], status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIsNone(response.data['data'])
        self.assertEqual(response.data['error'], 'Test Exception')
        self.assertEqual(response.data['message'], ['Error occurred while sending push notification.'])

    def test_send_push_invalid_payload(self):
        """
        Test sending a push notification with invalid payload data.
        """
        response = self.client.post(self.url('firebase'), self.invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data['errors'])
        self.assertIn('This field may not be blank.', response.data['errors']['title'])

    def test_send_push_unrecognized_service_type(self):
        """
        Test sending a push notification with an unrecognized service type.
        """
        response = self.client.post(self.url('unknown_service'), self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['status_code'], status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIsNone(response.data['data'])
        self.assertIn('service type is required', response.data['error'])
        self.assertEqual(response.data['message'], ['Error occurred while sending push notification.'])
