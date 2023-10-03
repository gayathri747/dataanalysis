"""
Import boto3 for accessing the AWS Services from python
If psycopg2 is not installed make sure to install it via the pip command mentioned in the README.md
"""
import boto3
import json
import pandas as pd
import psycopg2
import hashlib

"""
endpoint for the localstack is provided when we first run the docker run -p command this is used as url for connecting to the AWS services
It can be either AWS SQS, AWS S3 etc..
Dummy access key, secret and region is provided as we are using localstack if not AWS credentials are required.
"""
endpoint = 'http://localhost:4566/000000000000/login-queue'

botosession = boto3.Session(
    aws_access_key_id='ACCESS_ID_KEY',
    aws_secret_access_key='SECRET_ID_KEY',
    region_name='us-east-1',  
)
sqs = botosession.client('sqs', endpoint_url=endpoint)

"""
Queue URL is provided here for accessing the message queue of AWS SQS and reading the messages
Connection parameters for connecting to the postgres are provided here 
If incase hostname is not found run the below command and check the host name
docker inspect -f '{{.Config.Hostname}}' <container-id>
"""
queueurl = 'http://localhost:4566/000000000000/login-queue'

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='postgres',
    host='127.0.0.1',
    port='5432'
)

cursor = conn.cursor()
"""
SHA 256 is used as the masking technique to encode the PII data. This is one way encryption and decrypting takes a longer time

while there is a symmetric encryption  which requires a secured key which follows the 
"""
def maskpii(data):
    return hashlib.sha256(data.encode()).hexdigest()

while True:
    response = sqs.receive_message(
        QueueUrl=queueurl,
        AttributeNames=['All'],
        MaxNumberOfMessages=5,
        MessageAttributeNames=['All'],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    if 'Messages' in response:
        for message in response['Messages']:
            body = message['Body']
            message_body = json.loads(body)
            # print(message_body)
            insert_query = "INSERT INTO user_logins(user_id, app_version, device_type,masked_ip,locale, masked_device_id) VALUES (%s, %s,%s, %s,%s, %s)"
            cursor.execute(insert_query, (message_body['user_id'], message_body['app_version'], message_body['device_type'],maskpii(message_body['ip']),message_body['locale'],maskpii(message_body['device_id'])))
            conn.commit()
            print("Data inserted successfully.")
            # Delete the message from the queue to mark it as processed
            receipt = message['ReceiptHandle']
            sqs.delete_message(
                QueueUrl=queueurl,
                ReceiptHandle=receipt
            )
    else:
        print("No messages in the queue")
