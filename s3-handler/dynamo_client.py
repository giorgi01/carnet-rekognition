import json
import os
import uuid
from datetime import datetime

import boto3
from botocore.exceptions import ClientError


class DynamoClient:
    @staticmethod
    def save(data, db_name):
        dynamodb = boto3.client('dynamodb')
        timestamp = datetime.utcnow().isoformat()
        data_ready_to_be_saved = {
            'id': {
                'S': str(uuid.uuid1())
            },
            'createdAt': {
                'S': timestamp
            },
            'updatedAt': {
                'S': timestamp
            },
            'resultData': {
                'S': json.dumps(data)
            }
        }

        try:
            dynamodb.put_item(TableName=db_name, Item=data_ready_to_be_saved)
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise e
        return
