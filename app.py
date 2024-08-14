from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Path to the service account JSON key file
SERVICE_ACCOUNT_FILE = 'attendance-marker-432505-8e5cf4d3181b.json'

# Authenticate and create a client
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(credentials)

# Your Spreadsheet ID
SPREADSHEET_ID = '1oGcwqT-uqHmPRqq8acR7-w8RitnEA4Rd4_juVjs1ZMw'

@app.route('/')
def home():
    # Render the main page with your HTML template
    return render_template('index.html')

@app.route('/save_attendance', methods=['POST'])
def save_attendance():
    try:
        # Get JSON data from the request
        data = request.get_json()

        if not data or 'date' not in data:
            return jsonify({'error': 'Invalid data'}), 400

        # Open the Google Spreadsheet
        sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

        # Convert the data to a list
        attendance_data = [list(data.values())]

        # Append the data to the spreadsheet
        sheet.append_row(attendance_data[0])

        return jsonify({'message': 'Attendance saved successfully!'})

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': 'An error occurred while saving attendance'}), 500

if __name__ == '__main__':
    # Run the application on all addresses with port 8000
    app.run(host='0.0.0.0', port=8000, debug=True)
