from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Create a Flask blueprint for registration
register_bp = Blueprint('register', __name__)

# Route for registration
@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    message = None
    if request.method == 'POST':
        # Get user input from the registration form
        email = request.form['email']
        username = request.form['user_name']
        password = request.form['password']

        # API Gateway endpoint for the Lambda function
        api_gateway_endpoint = "https://1lepw5eofd.execute-api.ap-southeast-2.amazonaws.com/prod"
        
        # Prepare the payload for the request
        payload = {"email": email, "user_name": username, "password": password}
        
        # Send a POST request to the API Gateway
        response = requests.post(api_gateway_endpoint, json=payload)

        # Process the response
        if response.status_code == 200:
            if response.json().get("error"):
                error = response.json().get("error")
            else:
                message = 'User created, return to login!'
        else:
            error = "An error occurred during registration."

    return render_template('Register.html', error=error, message=message)
