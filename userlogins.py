"""
Import boto3 for accessing the AWS Services from python
If psycopg2 is not installed make sure to install it via the pip command mentioned in the README.md
"""
import boto3
import json
import pandas as pd
import psycopg2

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

# AWS SOS

# ------------------------------------------
# Specify the queue URL
queue_url = 'http://localhost:4566/000000000000/login-queue'

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='postgres',
    host='127.0.0.1',
    port='5432'
)

def mask_value(value):
    # Use a one-way hash function (SHA-256 in this example) to mask the value
    return hashlib.sha256(value.encode()).hexdigest()

# insert_query = "INSERT INTO user_logins_test (user_id, device_type, masked_ip, masked_device_id,locale, app_version) VALUES (%s, %s,%s, %s,%s, %s)"

cursor = conn.cursor()

# -------------------------------------------
# def trasnformdf(message_body):
#     key_value_pairs = []
#     for key, value in message_body.items():
#         key_value_pairs.append((key, value))
#         for key1, value1 in key_value_pairs:
#             print(key1,value1)
#             cursor.execute(insert_query, (key1, value1))
    
    # cursor.execute("INSERT INTO user_logins VALUES (%s, %s, %s, %s, %s, %s)", (
    #     data['user_id'],
    #     data['device_type'],
    #     data['masked_ip'],
    #     data['masked_device_id'],
    #     data['locale'],
    #     data['app_version']
    # ))

while True:
    # Receive messages from the queue (max 10 messages at a time)
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    if 'Messages' in response:
        # for message in response.get('Messages', []):
        for message in response['Messages']:
            body = message['Body']
            message_body = json.loads(body)
            # print(f"Received message: {body}")
            # print(message)
            # df = pd.read_json(body)
            print(message_body)
            insert_query = "INSERT INTO user_logins_test4 (user_id, app_version, device_type, ip,locale, device_id) VALUES (%s, %s,%s, %s,%s, %s)"
            cursor.execute(insert_query, (message_body['user_id'], message_body['app_version'], message_body['device_type'],mask_value(message_body['ip']),message_body['locale'],mask_value(message_body['device_id'])))
            conn.commit()
            print("Data inserted successfully.")
            # flattened_data = pd.json_normalize(message_body)
            # print(flattened_data) 
            # trasnformdf(message_body)

            # Process the message as needed

            # Delete the message from the queue to mark it as processed
            receipt_handle = message['ReceiptHandle']
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )

    else:
        print("No messages in the queue")
