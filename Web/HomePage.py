# Import necessary libraries and modules
from flask import Blueprint, render_template, redirect, session, request, jsonify, url_for
import boto3
import re
from boto3.dynamodb.conditions import Attr
import requests

# Define the blueprint for home routes
home_bp = Blueprint('home', __name__)

# Home route
@home_bp.route('/home')
def home(items=None, message=None, query=None):
    # Redirect user to login if email is not in session
    if 'email' not in session:
        return redirect('/')

    # API Gateway endpoint for getting user data
    api_gateway_endpoint = "https://wnv5sgkxbe.execute-api.ap-southeast-2.amazonaws.com/prod"
    payload = {"email": session['email']}
    headers = {'Content-Type': 'application/json'}  # Add headers for the request
    response = requests.post(api_gateway_endpoint, json=payload, headers=headers)

    # Check if the request is successful
    if response.status_code == 200:
        user_data = response.json()
        user_name = user_data['user_name']
        subscriptions_items = user_data['subscriptions_items']
    else:
        user_name = "Unknown"
        subscriptions_items = []

    # If there's a query, render template with query results
    if query:
        query_items = items
        query_message = message
        return render_template('HomePage.html', subscriptions_items=subscriptions_items, user_name=user_name, query_items=query_items, query_message=query_message)

    # Render home page template
    return render_template('HomePage.html', subscriptions_items=subscriptions_items, user_name=user_name)

# Query route
@home_bp.route('/query', methods=['POST', 'GET'])
def query():
    # Process POST request
    if request.method == 'POST':
        title = request.form['title']
        year = request.form.get('release_year')
        artist = request.form['artist']

        # API Gateway endpoint for querying items
        api_gateway_endpoint = "https://t8tyhbrjzl.execute-api.ap-southeast-2.amazonaws.com/prod"
        payload = {"title": title, "release_year": year, "artist": artist}
        response = requests.post(api_gateway_endpoint, json=payload)

        # Check if the request is successful
        if response.status_code == 200:
            items = response.json()['items']
            for item in items:
                artist_name = item['artist']
                artist_img = ''.join(x.capitalize() for x in re.split(r'[\W_]+', artist_name) if x)
                item['artist_img'] = "https://trapforment.s3.ap-southeast-2.amazonaws.com/"+artist_img+".jpg"

            message = ''
            if not items:
                message = 'No result is retrieved. Please query again.'
            return home(items, message=message, query=True)

        else:
            message = "An error occurred while querying."
            return render_template('HomePage.html', message=message)

    # Process GET request
    return home()

# Subscribe route
@home_bp.route('/subscribe', methods=['POST'])
def subscribe():
    title = request.form['title']
    release_year = request.form['release_year']
    artist = request.form['artist']
    img = request.form['artist_img']
    email = session['email']

    # API Gateway endpoint for subscribing
    api_gateway_endpoint = "https://znxaffrj2g.execute-api.ap-southeast-2.amazonaws.com/prod"
    payload = {"title": title, "release_year": release_year, "artist": artist, "artist_img": img, "email": email}
    response = requests.post(api_gateway_endpoint, json=payload)

    # Check if the request is successful
    if response.status_code != 200:
        message = "An error occurred while subscribing."
        return render_template('HomePage.html', message=message)

    # Return to the home route
    return home()

# Remove route
@home_bp.route('/remove', methods=['POST'])
def remove():
    title = request.form['title']
    email = session['email']

    # API Gateway endpoint for removing subscription
    api_gateway_endpoint = "https://2hrib70tuf.execute-api.ap-southeast-2.amazonaws.com/prod"
    payload = {"title": title, "email": email}
    response = requests.post(api_gateway_endpoint, json=payload)

    # Check if the request is successful
    if response.status_code != 200:
        message = "An error occurred while removing the subscription."
        return render_template('HomePage.html', message=message)

    # Return to the home route
    return home()

# Logout route
@home_bp.route('/logout')
def logout():
    session.pop('email', None)  # Remove email from the session
    return redirect(url_for('login.login'))
