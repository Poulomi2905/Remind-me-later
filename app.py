import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS # NEW: Import Flask-CORS

# Initialize Flask app
app = Flask(__name__)

# NEW: Enable CORS for your Flask app.
# This allows your frontend (loaded from a different origin, like file:// or localhost)
# to make requests to your API.
CORS(app)

# Configure the database
# Use SQLite for simplicity, store the database file in the project directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reminders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Reminder model
class Reminder(db.Model):
    """
    Represents a reminder entry in the database.
    Fields:
    - id: Primary key, auto-incrementing integer.
    - reminder_date: Date when the reminder should be sent (YYYY-MM-DD).
    - reminder_time: Time when the reminder should be sent (HH:MM).
    - message: The reminder message text.
    - reminder_type: How the reminder should be delivered (e.g., 'sms', 'email').
    - created_at: Timestamp when the reminder was created in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    reminder_date = db.Column(db.String(10), nullable=False) # Stored as YYYY-MM-DD
    reminder_time = db.Column(db.String(5), nullable=False)  # Stored as HH:MM
    message = db.Column(db.Text, nullable=False)
    reminder_type = db.Column(db.String(10), nullable=False) # 'sms' or 'email'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Reminder {self.id} - {self.reminder_date} {self.reminder_time}>'

    def to_dict(self):
        """
        Converts the Reminder object to a dictionary, suitable for JSON serialization.
        """
        return {
            'id': self.id,
            'reminder_date': self.reminder_date,
            'reminder_time': self.reminder_time,
            'message': self.message,
            'reminder_type': self.reminder_type,
            'created_at': self.created_at.isoformat() # Convert datetime to ISO format string
        }

# Create database tables before the first request
@app.before_request
def create_tables():
    """
    Ensures that database tables are created if they don't already exist.
    This runs before each request, but SQLAlchemy handles existing tables efficiently.
    """
    db.create_all()

@app.route('/')
def home():
    """
    Home route for basic API information.
    """
    return jsonify({"message": "Welcome to the Remind-Me-Later API!",
                    "endpoints": {
                        "POST /reminders": "Create a new reminder",
                        "GET /reminders": "Retrieve all reminders"
                    }})

@app.route('/reminders', methods=['POST'])
def create_reminder():
    """
    API endpoint to create a new reminder.
    Expects a JSON payload with:
    - reminder_date (string, YYYY-MM-DD)
    - reminder_time (string, HH:MM)
    - message (string)
    - reminder_type (string, 'sms' or 'email')

    Returns:
    - 201 Created on success with reminder ID.
    - 400 Bad Request on invalid input.
    """
    if not request.is_json:
        # Check if the request content type is JSON
        return jsonify({"status": "error", "message": "Content-Type must be application/json"}), 400

    data = request.get_json()

    # Validate required fields
    required_fields = ['reminder_date', 'reminder_time', 'message', 'reminder_type']
    for field in required_fields:
        if field not in data:
            return jsonify({"status": "error", "message": f"Missing field: {field}"}), 400

    reminder_date = data['reminder_date']
    reminder_time = data['reminder_time']
    message = data['message']
    reminder_type = data['reminder_type']

    # Basic data validation (can be expanded)
    # Date format YYYY-MM-DD
    try:
        datetime.strptime(reminder_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid reminder_date format. Use YYYY-MM-DD."}), 400

    # Time format HH:MM
    try:
        datetime.strptime(reminder_time, '%H:%M')
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid reminder_time format. Use HH:MM."}), 400

    # Reminder type validation
    if reminder_type not in ['sms', 'email']:
        return jsonify({"status": "error", "message": "Invalid reminder_type. Must be 'sms' or 'email'."}), 400

    try:
        # Create a new Reminder object
        new_reminder = Reminder(
            reminder_date=reminder_date,
            reminder_time=reminder_time,
            message=message,
            reminder_type=reminder_type
        )

        # Add to session and commit to database
        db.session.add(new_reminder)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Reminder saved successfully!",
            "id": new_reminder.id
        }), 201
    except Exception as e:
        # Rollback in case of any database error
        db.session.rollback()
        print(f"Error saving reminder: {e}")
        return jsonify({"status": "error", "message": "Failed to save reminder due to a server error."}), 500

@app.route('/reminders', methods=['GET'])
def get_reminders():
    """
    API endpoint to retrieve all existing reminders.

    Returns:
    - 200 OK with a list of reminder objects in JSON format.
    """
    try:
        # Query all reminders from the database, ordered by creation date
        reminders = Reminder.query.order_by(Reminder.created_at.asc()).all()

        # Convert each reminder object to a dictionary using the to_dict() method
        # This list of dictionaries will then be converted to JSON by jsonify
        reminders_list = [reminder.to_dict() for reminder in reminders]

        return jsonify({
            "status": "success",
            "message": "Reminders retrieved successfully!",
            "reminders": reminders_list
        }), 200
    except Exception as e:
        print(f"Error retrieving reminders: {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve reminders due to a server error."}), 500


# Run the app
if __name__ == '__main__':
    # This will create the database file (reminders.db) if it doesn't exist.
    # For development, debug=True provides useful error messages.
    app.run(debug=True)
