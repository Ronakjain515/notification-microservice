import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SendPushAPIViewTests(APITestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.url = reverse('send-push', kwargs={'service_type': 'firebase'})
        self.valid_payload = {
            "use_sqs": False,
            "payload": [
                {
                    'title': 'Test Title',
                    'content': 'Test Content',
                    'tokens': ['token1', 'token2'],
                    'extra_args': {'key': 'value'},
                    'badge_count': 1
                }
            ]
        }
        self.invalid_payload = {
            'title': '',
            'content': '',
            'tokens': [],
            'extra_args': {},
            'badge_count': -1
        }
        self.valid_auth_header = {'Authorization': 'Bearer PgNcfgxACIV7FOZPNL0rwroOm6Ut2eD0'}
        self.invalid_auth_header = {'Authorization': 'Bearer HsdfPgNcfgxACIV7FOZPNL0rwroOm6Ut2eD0'}

    def test_send_push_success(self):
        """
        Test successful push notification sending.
        """
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.valid_auth_header['Authorization']
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status_code'], status.HTTP_200_OK)
        self.assertIn('Push Notification', response.data['message'][0])

    def test_send_push_invalid_auth(self):
        """
        Test response when authorization header is invalid.
        """
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.invalid_auth_header['Authorization']
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_push_invalid_data(self):
        """
        Test response when invalid data is provided.
        """
        response = self.client.post(
            self.url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.valid_auth_header['Authorization']
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
