import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    SERVER_API = "API_ENDPOINT_FOR_SENDING_MESSAGE"
    API_KEY = "API_KEY"

    for record in event['Records']:
        message_body = record['body']

        logger.info(f"Processing message: {message_body}")

        try:
            headers = {
                "Authorization": f"Bearer {API_KEY}"
            }

            response = requests.post(
                SERVER_API,
                data={"json_string": message_body, "receipt_handle": record['receiptHandle']},
                headers=headers
            )

            logger.info(f"Status Code: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")

    return {
        "status_code": 200,
        "message": "Messages processed successfully!"
    }
