from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class SmsServiceAPIViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            "payload": [
                {
                    "send_to": "+1234567890",
                    "message": "Test message"
                }
            ]
        }
        self.invalid_payload = {
            "payload": [
                {
                    "send_to": "1234567890",  # Invalid phone number format
                    "message": "Test message"
                }
            ]
        }
        self.valid_auth_header = {'Authorization': 'Bearer PgNcfgxACIV7FOZPNL0rwroOm6Ut2eD0'}
        self.invalid_auth_header = {'Authorization': 'Bearer HsdfPgNcfgxACIV7FOZPNL0rwroOm6Ut2eD0'}
        self.url = reverse('send-sms', kwargs={'service_type': 'twilio'})

    def test_send_sms_valid_payload(self):
        """
        Test sending SMS with a valid payload.
        """

        response = self.client.post(
            self.url,
            data=self.valid_payload,
            format='json',
            HTTP_AUTHORIZATION=self.valid_auth_header['Authorization']
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["status_code"], status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Success")

    def test_send_sms_partial_failure(self):
        """
        Test sending SMS where some messages fail.
        """

        response = self.client.post(
            self.url,
            data=self.valid_payload,
            format='json',
            HTTP_AUTHORIZATION=self.valid_auth_header['Authorization']
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["status_code"], status.HTTP_200_OK)
        self.assertEqual(response.data["error"], "Failed Messages.")
        self.assertEqual(response.data["message"], "Success")
        self.assertEqual(len(response.data["data"]["failed_payload"]), 1)

    def test_invalid_service_type(self):
        """
        Test sending SMS with an invalid service type.
        """
        invalid_url = reverse('send-sms', kwargs={'service_type': 'invalid_service'})
        response = self.client.post(
            invalid_url,
            data=self.valid_payload,
            format='json',
            HTTP_AUTHORIZATION=self.valid_auth_header['Authorization']
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"][0], "Invalid service type.")

    def test_send_sms_invalid_payload(self):
        """
        Test sending SMS with an invalid payload.
        """
        response = self.client.post(
            self.url,
            data=self.valid_payload,
            format='json',
            HTTP_AUTHORIZATION=self.valid_auth_header['Authorization']
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["status_code"], status.HTTP_200_OK)
        self.assertEqual(response.data["error"], "Failed Messages.")
        self.assertEqual(response.data["message"], "Success")
        self.assertEqual(len(response.data["data"]["failed_payload"]), 1)
        self.assertIn("errors", response.data["data"]["failed_payload"][0])

    def test_send_sms_with_sqs(self):
        """
        Test sending SMS with SQS enabled.
        """
        payload_with_sqs = self.valid_payload.copy()
        payload_with_sqs["use_sqs"] = True

        response = self.client.post(
            self.url,
            data=self.valid_payload,
            format='json',
            HTTP_AUTHORIZATION=self.valid_auth_header['Authorization']
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status_code"], status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Success")
        self.assertEqual(len(response.data["data"]["failed_payload"]), 1)

