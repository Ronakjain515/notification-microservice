import os
import json
import boto3

from utilities.utils import logger

def push_message_to_sqs(message):
    print("sqs")
    sqs = boto3.client(
        'sqs',
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    )
    try:

        response = sqs.send_message(
            QueueUrl=os.getenv("SQS_URL"),
            MessageBody=json.dumps(message),
            DelaySeconds=10,
        )
        if response.get("ResponseMetadata").get("HTTPStatusCode", None) == 200:
            # Message sent successfully.
            logger.info("Message sent successfully to SQS.")

    except sqs.exceptions.InvalidMessageContents:
        # Invalid message content.
        logger.error("Message sent successfully to SQS.")

    except sqs.exceptions.UnsupportedOperation:
        # Unsupported operation.
        logger.error("Unsupported operation.")