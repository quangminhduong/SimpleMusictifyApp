import boto3
import json

# Lambda function handler
def lambda_handler(event, context):
    # Connect to DynamoDB and get the Subscriptions table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Subscriptions')
    
    # Parse the event object
    if 'body' in event:
        body = json.loads(event['body'])
    else:
        body = event
    
    # Extract subscription information
    title = body['title']
    release_year = body['release_year']
    artist = body['artist']
    img = body['artist_img']
    email = body['email']
    
    # Check if the subscription already exists
    existing_item = table.scan(
        FilterExpression="title = :title AND email = :email",
        ExpressionAttributeValues={
            ":title": title,
            ":email": email
        }
    )

    # If the subscription does not exist, add it to the table
    if not existing_item['Items']:
        # Get the highest ID value in the table
        response = table.scan(Select='SPECIFIC_ATTRIBUTES', ProjectionExpression="id")
        items = response['Items']

        if not items:
            index = 1
        else:
            max_value = max([item["id"] for item in items])
            index = max_value + 1

        # Create the new subscription item
        item = {
            'id': index,
            'title': title,
            'release_year': release_year,
            'artist': artist,
            'artist_img': img,
            'email': email
        }

        # Add the new subscription to the table
        table.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': json.dumps({'success': True})
    }

