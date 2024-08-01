# Import necessary libraries
import boto3
import json

# Function to validate user credentials
def validate_credentials(email, password):
    table = boto3.resource('dynamodb').Table('login')
    response = table.get_item(Key={'email': email})
    return response.get('Item') if 'Item' in response else None

# Lambda function handler
def lambda_handler(event, context):
    if 'body' in event:
        event = json.loads(event['body'])

    email = event['email']
    password = event['password']
    user = validate_credentials(email, password)
    if user:
        return {
            'statusCode': 200,
            'body': json.dumps({'success': True, 'user': user})
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'success': False, 'message': 'Email or password is invalid. Please try again.'})
        }
