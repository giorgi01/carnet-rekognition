import io
import os

import boto3
import json
import urllib3
import urllib3.request

from lambda_helper import LambdaHelper
from dynamo_client import DynamoClient


def analyze_image(image_url):
    http = urllib3.PoolManager()
    data = {'imageFile': image_url}  # Use 'img_url' as the key for the image URL

    url = 'https://carnet.ai/recognize-url'
    response = http.request('POST', url, fields=data)

    return LambdaHelper.handle_response(response)


def lambda_handler(event, _):
    s3_client = boto3.client("s3")

    recs = event['Records']
    for record in recs:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        location = s3_client.get_bucket_location(Bucket=bucket)['LocationConstraint']
        url = f'https://{bucket}.s3.{location}.amazonaws.com/{key}'

        result = analyze_image(url)

        if result is not None:
            DynamoClient.save(result, os.getenv('CARNET_DB'))
        else:
            result = LambdaHelper.generate_image_labels(bucket, key)
            DynamoClient.save(result, os.getenv('REKOGNITION_DB'))

    return {"statusCode": 200, "body": "OK"}
