# Import necessary libraries and modules
from flask import Flask
from flask_cors import CORS

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)  # Enable CORS
app.secret_key = 'secret_key_will_be_here_at_some_point'

# Register blueprints
from Login import login_bp
app.register_blueprint(login_bp)

from HomePage import home_bp
app.register_blueprint(home_bp)

from Register import register_bp
app.register_blueprint(register_bp)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
