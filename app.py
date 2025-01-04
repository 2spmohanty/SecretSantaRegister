from flask import Flask
from models import db  # Import db from models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secret_santa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to suppress a warning

# Initialize the db with the app
db.init_app(app)

# Import routes after initializing db
from routes import *

if __name__ == '__main__':
    with app.app_context():  # Create an application context
        db.create_all()  # Create all tables
        print("Database initialized!")  # Optional confirmation message
    app.run(debug=True,port=8000)