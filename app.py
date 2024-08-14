import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'attendance-marker-432505-8e5cf4d3181b.json'

# Authenticate and create a client
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(credentials)

# Your Spreadsheet ID
SPREADSHEET_ID = '1oGcwqT-uqHmPRqq8acR7-w8RitnEA4Rd4_juVjs1ZMw'

@app.route('/')
def home():
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
        
        # Convert JSON data to DataFrame
        attendance_data = pd.DataFrame(list(data.items()), columns=['Student', 'Attendance'])

        # Read existing data from Google Sheets into a DataFrame
        existing_data = pd.DataFrame(sheet.get_all_records())

        # Extract fixed columns
        if 'USN' not in existing_data.columns:
            existing_data['USN'] = ''
        if 'Student Name' not in existing_data.columns:
            existing_data['Student Name'] = ''

        # Process the date
        date_column = data.get('date')
        if date_column not in existing_data.columns:
            existing_data[date_column] = ''

        # Update attendance data
        for _, row in attendance_data.iterrows():
            student = row['Student']
            attendance = row['Attendance']
            existing_data.loc[existing_data['Student Name'] == student, date_column] = attendance

        # Update Google Sheets
        sheet.update([existing_data.columns.tolist()] + existing_data.values.tolist())

        return jsonify({'message': 'Attendance saved successfully!'})

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': 'An error occurred while saving attendance'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
