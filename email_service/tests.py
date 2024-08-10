from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

class SendEmailAPIViewTests(TestCase):
    def setUp(self):
        """
        Initialize the API client and any necessary setup for the tests.
        """
        self.client = APIClient()
        self.url = '/send/'  # Adjust this based on your URL configuration
        self.valid_data = {
            'to': ['sandeep.negi@mindbowser.com', 'ravi.mourya@mindbowser.com'],
            'cc': ['ronak.jain@mindbowser.com'],
            'bcc': ['shubham.yadav@mindbowser.com'],
            'subject': 'Test Subject',
            'message': 'Test Message',
            'template_id': 'd-cb04b0e0fbf84197a707403456965fc3',
            'dynamic_template_data': {'title': 'Accelathon', 'subject': 'Mindbowser'},
            'attachments': []
        }
        self.invalid_provider_type = 'sendbird'
        self.valid_provider_type = 'sendgrid'
        self.email_choices = ['sendgrid', 'smtp']
        self.valid_auth_header = {'Authorization': 'Bearer PgNcfgxACIV7FOZPNL0rwroOm6Ut2eD0'}
        self.invalid_auth_header = {'Authorization': 'Bearer PgNcfgxACIV7FOZPNL0rwroOm6Ut2eD034yer'}


    @patch('path.to.EmailService.send_email')
    def test_send_email_success(self, mock_send_email):
        """
        Test that the email is sent successfully.
        """
        mock_send_email.return_value = (True, 'Success', {})
        response = self.client.post(self.url, data=self.valid_data, format='json', HTTP_PROVIDER_TYPE=self.valid_provider_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], ['Email sent successfully.'])

    @patch('path.to.EmailService.send_email')
    def test_send_email_failure(self, mock_send_email):
        """
        Test that the email sending fails and returns an error.
        """
        mock_send_email.return_value = (False, 'Failed', {})
        response = self.client.post(self.url, data=self.valid_data, format='json', HTTP_PROVIDER_TYPE=self.valid_provider_type)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], ['Failed'])

    def test_invalid_provider_type(self):
        """
        Test that an invalid provider type results in a validation error.
        """
        response = self.client.post(self.url, data=self.valid_data, format='json', HTTP_PROVIDER_TYPE=self.invalid_provider_type)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], 'Invalid provider_type.')

    def test_missing_required_fields(self):
        """
        Test that missing required fields returns a validation error.
        """
        invalid_data = {
            'to': []
            # Missing other required fields
        }
        response = self.client.post(self.url, data=invalid_data, format='json', HTTP_PROVIDER_TYPE=self.valid_provider_type)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('to', response.data)
        self.assertIn('subject', response.data)
        self.assertIn('message', response.data)

    @patch('path.to.EmailService.send_email')
    def test_email_service_call(self, mock_send_email):
        """
        Test that the EmailService.send_email method is called with the correct arguments.
        """
        mock_send_email.return_value = (True, 'Success', {})
        response = self.client.post(self.url, data=self.valid_data, format='json', HTTP_PROVIDER_TYPE=self.valid_provider_type)
        mock_send_email.assert_called_once_with(
            ['sandeepnegi1710@gmail.com'],
            'Test Subject',
            'Test Message',
            'd-cb04b0e0fbf84197a707403456965fc3',
            {'title': 'Mindbowser'},
            'sendgrid',
            ['shubham.yadav@mindbowser.com'],
            ['ronak.jain@mindbowser.com'],
            []
        )

    # Add more tests as necessary for other scenarios or edge cases
