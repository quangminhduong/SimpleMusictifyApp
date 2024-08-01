# Import necessary libraries and modules
from flask import Blueprint, request, render_template, redirect, session, url_for
import requests

# Define the blueprint for login routes
login_bp = Blueprint('login', __name__)

# Function to validate user credentials
def validate_credentials(email, password):
    api_gateway_endpoint = "https://j9foxa3938.execute-api.ap-southeast-2.amazonaws.com/prod"
    payload = {"email": email, "password": password}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_gateway_endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("user") 
    else:
        return None

# Login route
@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = validate_credentials(email, password)
        if user:
            session['email'] = email  # Store email in the session
            return redirect(url_for('home.home'))
        else:
            error_msg = "Email or password is invalid. Please try again."
            return render_template('Login.html', error=error_msg)
    else:
        return render_template('Login.html')
