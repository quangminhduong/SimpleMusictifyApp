import boto3
import json

# Lambda function handler
def lambda_handler(event, context):
    # Connect to DynamoDB and get the login table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('login')
    
    # Parse the event object
    if 'body' in event:
        event = json.loads(event['body'])

    # Extract user information
    email = event['email']
    username = event['user_name']
    password = event['password']
    
    # Check if the email already exists
    response = table.get_item(Key={'email': email})

    if 'Item' in response:
        # Email already exists, return an error
        return {
            'statusCode': 400,
            'body': json.dumps({'success': False, 'message': 'Email already exists!'})
        }
    else:
        # Add the new user to the login table
        table.put_item(Item={'email': email, 'user_name': username, 'password': password})
        return {
            'statusCode': 200,
            'body': json.dumps({'success': True, 'message': 'User created, return to login!'})
        }
