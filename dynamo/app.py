import json
import boto3
import decimal

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table("User-Logging")

    res = table.get_item(Key={'id': '1'})

    return {
        'statusCode': 200,
        'body': json.dumps(res, cls=Encoder)
    }


def lambda_two_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table("User-Logging")

    item = json.loads((event["body"]), parse_float=decimal.Decimal)

    table.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': json.dumps(item, cls=Encoder)
    }
