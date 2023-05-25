import json


def lambda_handler(event, _):
    return {
        'statusCode': 200,
        'body': json.dumps('There goes carnet handla')
    }
