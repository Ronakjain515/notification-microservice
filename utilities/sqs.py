import os
import json
import boto3
from botocore.exceptions import ClientError

from utilities.utils import logger, CustomException


try:
    sqs = boto3.client(
        'sqs',
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    )
except Exception:
    sqs = None


def push_message_to_sqs(message):
    if sqs is None:
        CustomException("SQS is not setup.")
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


def receiver_message_sqs(receipt_handle):
    """
    Retrieve a message from an SQS queue using the receipt handle.

    :param receipt_handle: The receipt handle of the message to retrieve.
    :return: The message body if successful, otherwise None.
    """
    if sqs is None:
        CustomException("SQS is not setup.")
    try:
        # Receive the message from the queue
        response = sqs.receive_message(
            QueueUrl=os.getenv("SQS_URL"),
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )

        # Check if messages are returned
        messages = response.get('Messages', [])
        if not messages:
            print("No messages in the queue.")
            return None

        # Loop through messages and find the one with the matching receipt handle
        for message in messages:
            if message['ReceiptHandle'] == receipt_handle:
                sqs.delete_message(
                    QueueUrl=os.getenv("SQS_URL"),
                    ReceiptHandle=receipt_handle
                )
                # Print out the message body
                print(f"Message received: {message['Body']}")
                return message['Body']

        print("No message found with the given receipt handle.")
        return None

    except ClientError as e:
        print(f"An error occurred: {e}")
        return None
