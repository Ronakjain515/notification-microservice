import os
from dotenv import load_dotenv
import boto3

load_dotenv()


def send_message_to_sqs(sqs, sqs_url, message_body, count=100):
    try:
        for i in range(count):
            # Send a message to the specified SQS queue
            response = sqs.send_message(
                QueueUrl=sqs_url,
                MessageBody=f"{message_body} {i+1}"
            )
            print(f"Message {i+1} sent! Message ID:", response['MessageId'])

    except Exception as e:
        print("Error sending message to SQS:", e)


def delete_message_from_sqs(sqs, sqs_url):
    try:
        # Receive a single message from the queue
        response = sqs.receive_message(
            QueueUrl=sqs_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5
        )

        messages = response.get('Messages', [])
        if messages:
            message = messages[0]
            receipt_handle = message['ReceiptHandle']
            print("Received message:", message['Body'])

            # Delete the message from the queue
            sqs.delete_message(
                QueueUrl=sqs_url,
                ReceiptHandle=receipt_handle
            )
            print("Message deleted!")
        else:
            print("No messages to delete.")

    except Exception as e:
        print("Error receiving or deleting messages:", e)


def main():
    # Get AWS credentials and region from environment variables
    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_secret_key = os.getenv('AWS_SECRET_KEY')
    aws_region = os.getenv('AWS_REGION')
    sqs_url = os.getenv('SQS_URL')
    message_body = input("Enter the message to send: ")

    # Create a session and SQS client
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )
    sqs = session.client('sqs')

    # Send messages to the queue
    send_message_to_sqs(sqs, sqs_url, message_body)

    # Delete a message from the queue
    delete_message_from_sqs(sqs, sqs_url)


if __name__ == "__main__":
    main()
