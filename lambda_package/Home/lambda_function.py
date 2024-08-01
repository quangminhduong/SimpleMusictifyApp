# Import necessary libraries
import boto3
import json
import re
from boto3.dynamodb.conditions import Attr
import decimal

# Create a JSONEncoder class to handle Decimal objects from DynamoDB
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

# Function to get the user name by email
def get_user_name(email):
    # Access the 'login' DynamoDB table
    table = boto3.resource('dynamodb').Table('login')
    response = table.get_item(Key={'email': email})
    item = response.get('Item')
    if not item:
        return None
    user_name = item['user_name']
    return user_name

# Function to get the subscriptions of a user by email
def get_subscriptions(email):
    dynamodb = boto3.resource('dynamodb')
    subscriptions_table = dynamodb.Table('Subscriptions')
    subscriptions_response = subscriptions_table.scan(
        FilterExpression=Attr('email').eq(email)
    )
    subscriptions_items = subscriptions_response.get('Items', [])
    return subscriptions_items

# Main Lambda function handler
def lambda_handler(event, context):
    if 'body' in event:
        body = json.loads(event['body'])
        email = body['email']
    else:
        email = event['email']

    user_name = get_user_name(email)
    if not user_name:
        return {
            'statusCode': 404,
            'body': json.dumps({'success': False, 'message': 'Email not found'}, cls=DecimalEncoder)  
        }
    subscriptions_items = get_subscriptions(email)
    return {
        'statusCode': 200,
        'body': json.dumps({
            'success': True,
            'user_name': user_name,
            'subscriptions_items': subscriptions_items
        }, cls=DecimalEncoder)  
    }
