import boto3
import json
import re

# Lambda function handler
def lambda_handler(event, context):
    # Parse the event object
    if 'body' in event:
        data = json.loads(event['body'])
    else:
        data = event

    # Extract search criteria
    title = data.get('title', '')
    year = data.get('release_year', '')
    artist = data.get('artist', '')

    # Check if at least one search criteria is provided
    if not title and not year and not artist:
        return {
            'statusCode': 400,
            'body': json.dumps({'success': False, 'message': 'Please enter data in at least one of the fields.'})
        }

    # Connect to DynamoDB and get the music table
    dynamodb = boto3.resource('dynamodb')
    music_table = dynamodb.Table('music')

    # Initialize filter expressions and values
    filters = []
    values = {}

    # Add filters based on provided search criteria
    if title:
        filters.append("contains(title, :title)")
        values[':title'] = title

    if year:
        filters.append("contains(release_year, :release_year)")
        values[':release_year'] = year

    if artist:
        filters.append("contains(artist, :artist)")
        values[':artist'] = artist

    # Combine filter expressions with OR
    filter_expression = " OR ".join(filters)

    # Scan the music table with the filter expressions
    response = music_table.scan(
        FilterExpression=filter_expression,
        ExpressionAttributeValues=values
    )

    # Extract items from the response
    items = response['Items']
    # Append artist image URL to each item
    for item in items:
        artist_name = item['artist']
        artist_img = ''.join(x.capitalize() for x in re.split(r'[\W_]+', artist_name) if x)
        item['artist_img'] = "https://trapforment.s3.ap-southeast-2.amazonaws.com/"+artist_img+".jpg"

    # Set message if no items are found
    message = ''
    if not items:
        message = 'No result is retrieved. Please query again.'

    # Return the result as a JSON object
    return {
        'statusCode': 200,
        'body': json.dumps({
            'success': True,
            'items': items,
            'message': message
        })
    }
