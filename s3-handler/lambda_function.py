import io
import boto3
import json

from lambda_helper import LambdaHelper
from dynamo_client import DynamoClient


def analyze_image(img_url):
    client = boto3.client('lambda')
    payload = {
        "httpMethod": "POST",
        "body": img_url,
        "url": 'https://carnet.ai/recognize-image_url'
    }
    payload = json.dumps(payload).encode('utf-8')

    response = client.invoke(
        FunctionName='carnet-handler',
        InvocationType='RequestResponse',
        Payload=payload
    )

    return LambdaHelper.handle_response(response)


def lambda_handler(event, _):
    s3_client = boto3.client("s3")

    for record in event.get("Records"):
        bucket = record.get("s3").get("bucket").get("name")
        key = record.get("s3").get("object").get("key")
        location = boto3.client('s3').get_bucket_location(Bucket=bucket)['LocationConstraint']
        url = f'https://{bucket}.s3.{location}.amazonaws.com/{key}'

        file = io.BytesIO()
        s3_client.download_fileobj(Bucket=bucket, Key=key, Fileobj=file)
        file.seek(0)

        result = analyze_image(url)
        print("result", result)  # debug purpouses

        DynamoClient.save(result)

    return {"statusCode": 200, "body": "OK"}
