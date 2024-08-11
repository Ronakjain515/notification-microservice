# Notification Microservice

This microservice handles sending notifications across three channels: SMS, email, and push notifications. It supports various providers for each notification type, allowing for flexible integration with different services.

## Supported Notifications and Providers

1. **SMS Notifications**:
   - **Provider**: Twilio

2. **Email Notifications**:
   - **Providers**: SMTP, SendGrid

3. **Push Notifications**:
   - **Provider**: Firebase

## APIs

### 1. Send SMS Notifications

- **Endpoint**: `/api/sms/{service_type}/`
- **Method**: `POST`
- **Description**: Sends SMS messages using the specified service (`twilio`).
- **Parameters**:
  - `service_type`: The SMS service provider (`twilio`).
  - `payload`: List of message objects, each containing:
    - `send_to`: List of phone numbers.
    - `message`: Content of the SMS.
  - `use_sqs`: Optional boolean to determine if the message should be pushed to an SQS queue.

**Example Request**:
```json
{
  "use_sqs": false,
  "payload": [
    {
      "send_to": ["+1234567890"],
      "message": "Hello from Twilio!"
    }
  ]
}
```

### 2. Send Email Notifications

- **Endpoint**: `/api/email/{provider_type}/`
- **Method**: `POST`
- **Description**: Sends emails using the specified provider (`smtp` or `sendgrid`).

#### URL Parameters

- `provider_type`: The email service provider (`smtp` or `sendgrid`).

#### Request Body

- `use_sqs` (optional, boolean): Determines if the email data should be pushed to an SQS queue.
- `payload`: List of email objects, each containing:
  - `to`: List of recipient email addresses.
  - `subject`: Subject of the email.
  - `message`: Body of the email.
  - `template_id` (optional, for SendGrid): ID of the email template to use.
  - `dynamic_template_data` (optional, for SendGrid): Data to populate dynamic fields in the email template.
  - `cc` (optional): List of CC email addresses.
  - `bcc` (optional): List of BCC email addresses.
  - `attachments` (optional): List of file attachments to include in the email.

#### Example Request

```json
{
  "use_sqs": false,
  "payload": [
    {
      "to": ["example@example.com"],
      "subject": "Test Email",
      "message": "This is a test email.",
      "template_id": "d-1234567890abcdef1234567890abcdef",
      "dynamic_template_data": {
        "name": "John Doe",
        "event": "Webinar"
      },
      "cc": ["cc@example.com"],
      "bcc": ["bcc@example.com"],
      "attachments": [
        {
          "filename": "attachment.pdf",
          "content": "<base64-encoded-content>",
          "type": "application/pdf"
        }
      ]
    }
  ]
}
```
### 3. Send Push Notifications

- **Endpoint**: `/api/push/{service_type}/`
- **Method**: `POST`
- **Description**: Sends push notifications using the specified service type (`firebase` or `sns`).

#### URL Parameters

- `service_type`: The push notification service (`firebase` or `sns`).

#### Request Body

- `use_sqs` (optional, boolean): Determines if the push notification data should be pushed to an SQS queue.
- `payload`: List of push notification objects, each containing:
  - `title`: Title of the push notification.
  - `content`: Content or body of the push notification.
  - `extra_args` (optional): Additional arguments or data to include in the notification.
  - `tokens`: List of device tokens to which the notification should be sent.
  - `badge_count` (optional): Badge count for the notification.

#### Example Request

```json
{
  "use_sqs": false,
  "payload": [
    {
      "title": "Important Update",
      "content": "Your account has been updated.",
      "extra_args": {
        "action": "update",
        "details": "Account details have changed."
      },
      "tokens": ["token1", "token2"],
      "badge_count": 1
    }
  ]
}
```

## Setup and Configuration

### Prerequisites

Before setting up the microservice, ensure you have the following prerequisites:

- **Python**: Version 3.7 or later
- **Django**: Version 3.0 or later
- **Django REST Framework**: Version 3.11 or later
- **Other Libraries**: Install required libraries using `requirements.txt`

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-repository-url.git
   ```

2. **Navigate to the project directory**
    ```bash
    cd <project-directory>
    ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the environment variables as described above.**


### Running the Service

1**Start the server**

```bash
python manage.py runserver
```

2**Access the API endpoints via your preferred HTTP client (e.g., Postman) or using the provided Swagger documentation.**


## Error Handling

1. Invalid Provider: Returns an error if the specified provider is not supported.
2. Validation Errors: Returns details of validation issues in the request payload.
3. Service Errors: Logs and returns errors from the respective service providers.

## Contributing
1. Fork the repository.
2. Create a new branch.
3. Make your changes and test them.
4. Submit a pull request with a description of the changes.

