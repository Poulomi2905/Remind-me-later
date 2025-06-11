# Remind-me-later
Project Overview
The "Remind Me Later" is a simple web application designed to help users set and manage personal reminders. Users can specify a reminder message, a date, and a time, and choose how they'd like to be reminded (currently via SMS or Email, though actual delivery logic is not implemented in this version). The application features a Python Flask API for backend data storage and a responsive frontend built with HTML, Tailwind CSS, and JavaScript.

This project was developed as part of an initial screening exercise, focusing on API design, backend implementation with a database, and basic frontend integration.

Features
Set Reminders: Users can input a message, select a specific date and time, and choose a reminder type (SMS or Email).

Store Reminders: All reminder details are persistently stored in a local SQLite database.

View Reminders: The application retrieves and displays a list of all scheduled reminders from the database on the frontend.

Simple & Responsive UI: A clean, user-friendly interface that adapts to different screen sizes.

Tech Stack
Backend (API)
Python: The core programming language.

Flask: A lightweight Python web framework for building the API endpoints.

Flask-SQLAlchemy: An extension for Flask that simplifies working with SQLAlchemy, an Object-Relational Mapper (ORM), for database interactions.

SQLite: A file-based SQL database used for persistent storage of reminder data.

Flask-CORS: An extension to handle Cross-Origin Resource Sharing, allowing the frontend (served from a different origin) to communicate with the Flask API.

Frontend (User Interface)
HTML5: Structures the content of the web page.

CSS3 (Tailwind CSS): Provides rapid and responsive styling.

JavaScript (ES6+): Handles dynamic interactions, form submissions, and communication with the backend API using the fetch API.

Setup & Installation
Follow these steps to get the "Remind Me Later App" running on your local machine.

Prerequisites
Python 3.8+ installed on your system.

pip (Python package installer) installed.

VS Code (or any preferred code editor) recommended.

Steps
Clone the Repository (or download the files):
If you're using Git, clone this repository to your local machine:

git clone <repository_url>
cd remind-me-later-app

(Replace <repository_url> with the actual URL of your GitHub repository.)
If you've downloaded the files, navigate to the project directory in your terminal.

Create a Virtual Environment (Recommended):
It's best practice to use a virtual environment to manage project dependencies.

python -m venv venv

Activate the Virtual Environment:

Windows:

.\venv\Scripts\activate

macOS/Linux:

source venv/bin/activate

You should see (venv) at the beginning of your terminal prompt, indicating the virtual environment is active.

Install Python Dependencies:
With your virtual environment active, install all the required Flask extensions:

pip install Flask Flask-SQLAlchemy Flask-CORS

How to Run the Application
The application consists of two main parts: the Flask backend API and the HTML/JavaScript frontend. Both need to be running/opened for the full experience.

1. Run the Backend API
Open your terminal or Command Prompt.

Navigate to the project directory where app.py is located.

Example (Windows, assuming Poulomi is your username):

cd "C:\Users\Poulomi\Documents\Symplique solutions"

Make sure your virtual environment is activated as per step 3 in "Setup & Installation".

Run the Flask application:

python app.py

You should see output similar to this, indicating the server is running:

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit

Keep this terminal window open as long as you want the API to be accessible.

2. Open the Frontend
Navigate to the project directory in your file explorer (e.g., Windows Explorer, macOS Finder).

Double-click on the index.html file.

This will open the web application in your default web browser.

API Endpoints
The Flask backend provides the following RESTful API endpoints:

GET /

Description: Home route, provides basic information about the API and available endpoints.

Response: JSON object with API status and endpoint details.

POST /reminders

Description: Creates a new reminder entry in the database.

Request Body (JSON):

{
    "reminder_date": "YYYY-MM-DD",  // e.g., "2025-07-20"
    "reminder_time": "HH:MM",      // e.g., "14:30"
    "message": "string",           // The reminder message
    "reminder_type": "string"      // "sms" or "email"
}

Response (JSON):

201 Created on success: {"status": "success", "message": "Reminder saved successfully!", "id": 1}

400 Bad Request on invalid input.

GET /reminders

Description: Retrieves all existing reminders from the database.

Response (JSON):

200 OK with a list of reminder objects:

{
  "status": "success",
  "message": "Reminders retrieved successfully!",
  "reminders": [
    {
      "created_at": "2025-06-11T12:35:00.000000",
      "id": 1,
      "message": "Call Grandma for her birthday!",
      "reminder_date": "2025-07-20",
      "reminder_time": "14:30",
      "reminder_type": "sms"
    },
    // ... more reminder objects
  ]
}

Usage
Set a Reminder:

On the index.html page, fill in the "Reminder Date", "Reminder Time", "Message", and select "Remind Via".

Click the "Set Reminder" button.

A success message will appear, and your new reminder will be added to the "Your Scheduled Reminders" list below.

View Reminders:

Reminders will automatically load when the page is opened.

Click the "Refresh Reminders" button to fetch the latest list of reminders from the API.

Future Enhancements (Potential Next Steps)
Actual Message Delivery: Implement logic to send SMS (e.g., using Twilio) and Email (e.g., using Flask-Mail with an SMTP server) at the scheduled time. This would require a background task runner (e.g., Celery, APScheduler).

User Authentication & Authorization: Add user registration, login, and ensure users can only manage their own reminders.

CRUD Operations: Implement PUT (Update) and DELETE functionality for reminders via new API endpoints and corresponding frontend UI.

Improved Frontend Features: Add pagination, filtering, or sorting for the reminders list.

Error Handling & UI Feedback: More sophisticated error messages and loading indicators for a better user experience.

Deployment: Prepare the application for deployment to a cloud platform (e.g., Heroku, AWS, Google Cloud).
