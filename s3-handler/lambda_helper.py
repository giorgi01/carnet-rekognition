import time

import boto3


class LambdaHelper:
    @staticmethod
    def handle_response(r):
        code = r.status
        match code:
            case 200:
                data = r.data.read().decode('utf-8')
                return data
            case 429:
                print("Bad API response: 429. Retrying...")
                time.sleep(1)
            case _:
                print(f"Bad API response: {code} - {r.reason}")

    @staticmethod
    def generate_image_labels(bucket, key):
        client = boto3.client('rekognition')
        return client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            },
            MaxLabels=20)

