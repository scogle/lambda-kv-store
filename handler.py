"""
AWS Lambda Handler Module

Reads and Writes to a key/value store backed by DynamoDB

Author: Scott Ogle <scottogle@gmail.com>
"""

import json
import boto3
from decimal import Decimal

from pprint import pprint

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('nike-test')

class DecimalEncoder(json.JSONEncoder):
    """
    Quick and dirty solution taken from:
    https://stackoverflow.com/questions/43678946/python-3-x-cannot-serialize-decimal-to-json
    """
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def form_http_response(status, body):
    return {
        "statusCode": status,
        "headers": { "Content-Type": "application/json" },
        "body": json.dumps(body, cls=DecimalEncoder)
    }


def ping(event, context):
    """
    Route to quickly check service status
    """
    body = {"message": "PONG"}
    return form_http_response(200, body)


def get_all_keys(event, context):
    """
    List all key/value pairs
    """
    db_response = table.scan()
    items = db_response['Items']

    return form_http_response(200, items)


def get_key(event, context):
    """
    Returns a single key/value pair by key
    @params:
        key: Required, specifies the key of the key/value pair to return
    """
    key = event['pathParameters']['key']

    db_response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('key').eq(key)
    )
    items = db_response['Items']
    if len(items) == 0:
        return form_http_response(404, {"error": "key not found"})
    return form_http_response(200, items[0])


def add_key(event, context):
    """
    Adds a single key/value pair
    @params:
        key: Required, specifies the key of the key/value pair to create
        value: Required, sets the key's value. Defaults to True if a value is not supplied
    """
    key = event['pathParameters']['key']
    value = event.get('queryStringParameters', {}).get('value', None)

    db_response = table.put_item(
        Item={
            'key': key,
            'value': value
        }
    )

    body = {"message": "success"}
    return form_http_response(200, body)


def update_key(event, context):
    """
    Updates a single key/value pair
    @params:
        key: Required, specifies the key of the key/value pair to create
        value: Required, sets the key's value
    """
    key = event['pathParameters']['key']
    value = event.get('queryStringParameters', {}).get('value', None)

    if value is None:
        return {
            "statusCode": 400,
            "body": {"error": "Missing required query string parameter 'value'"}
        }

    db_response = table.update_item(
        Key={"key": key},
        AttributeUpdates={
            "value": {
                'Value': value
            }
        }
    )

    body = {"message": "success"}
    return form_http_response(200, body)


def delete_key(event, context):
    """
    Deletes a single key/value pair
    @params:
        key: Required, specifies the key of the key/value pair to create
    """
    key = event['pathParameters']['key']

    table.delete_item(
        Key={
            'key': key
        }
    )

    body = {"message": "success"}
    return form_http_response(200, body)


