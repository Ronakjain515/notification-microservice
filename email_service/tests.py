import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class SendEmailAPIViewTests(APITestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.url = reverse('send-email', kwargs={'provider_type': 'sendgrid'})
        self.valid_payload = {
            "use_sqs": True,
            "payload": [{
                'to': ['sandeep.negi@mindbowser.com', 'ravi.mourya@mindbowser.com'],
                'cc': ['ronak.jain@mindbowser.com'],
                'bcc': ['shubham.yadav@mindbowser.com'],
                'subject': 'Test Subject',
                'message': 'Test Message',
                'template_id': 'd-cb04b0e0fbf84197a707403456965fc3',
                'dynamic_template_data': {'title': 'Accelathon', 'subject': 'Mindbowser'},
                'attachments': []
            }]
        }
        self.invalid_payload = {
            "use_sqs": False,
            "payload": [{
                'to': [],
                'cc': [],
                'bcc': [],
                'subject': '',
                'message': '',
                'template_id': '',
                'dynamic_template_data': {},
                'attachments': []
            }]
        }
        self.valid_auth_header = {'Authorization': 'Bearer PgNcfgxACIV7FOZPNL0rwroOm6Ut2eD0'}
        self.invalid_auth_header = {'Authorization': 'Bearer HsdfPgNcfgxACIV7FOZPNL0rwroOm6Ut2eD0'}

    def test_send_email_success(self):
        """
        Test successful email sending.
        """
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.valid_auth_header['Authorization']
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status_code'], status.HTTP_200_OK)
        self.assertIn('Email sent successfully', response.data['message'][0])

    def test_send_email_invalid_auth(self):
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

    def test_send_email_invalid_data(self):
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
