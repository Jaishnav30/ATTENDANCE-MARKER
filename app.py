import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Setup Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_service_account.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("Your Google Sheet Name").sheet1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save_attendance', methods=['POST'])
def save_attendance():
    try:
        data = request.get_json()
        if not data or 'date' not in data:
            return jsonify({'error': 'Invalid data'}), 400

        date = data.get('date')

        # Convert the data to a DataFrame and append to the Google Sheet
        df = pd.DataFrame([data])
        sheet.append_row(df.iloc[0].values.tolist())

        return jsonify({'message': 'Attendance saved successfully!'})

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': 'An error occurred while saving attendance'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
