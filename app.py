from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

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

        date = data.get('date')
        # Prepare the data to be saved
        df = pd.DataFrame([data])
        file_path = 'attendance_data.xlsx'

        if os.path.exists(file_path):
            # Load existing data and append new data
            with pd.ExcelFile(file_path) as xls:
                existing_df = pd.read_excel(xls, sheet_name='Sheet1')
                df = pd.concat([existing_df, df], ignore_index=True)

        # Save to Excel file
        df.to_excel(file_path, sheet_name='Sheet1', index=False)

        return jsonify({'message': 'Attendance saved successfully!'})

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': 'An error occurred while saving attendance'}), 500

if __name__ == '__main__':
    # Run the application on all addresses with port 8000
    app.run(host='0.0.0.0', port=8000, debug=True)
