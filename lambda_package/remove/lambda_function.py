import boto3
import json

# Lambda function handler
def lambda_handler(event, context):
    # Connect to DynamoDB and get the Subscriptions table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Subscriptions')

    # Parse the event object
    if 'body' in event:
        event = json.loads(event['body'])

    # Extract subscription information
    title = event['title']
    email = event['email']

    # Check if the subscription already exists
    response = table.scan(
        FilterExpression='title = :title and email = :email',
        ExpressionAttributeValues={
            ':title': title,
            ':email': email
        }
    )

    # Delete the subscription if found
    if response['Count'] == 1:
        item_id = response['Items'][0]['id']
        table.delete_item(Key={'id': item_id})

    return {
        'statusCode': 200,
        'body': json.dumps({'success': True})
    }
