from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    # Render the main page with your HTML template
    return render_template('index.html')

@app.route('/save_attendance', methods=['POST'])
def save_attendance():
    # Get JSON data from the request
    data = request.get_json()
    
    # Extract attendance data and date
    attendance_data = data
    date = attendance_data.get('date')
    
    # Prepare the data to be saved
    df = pd.DataFrame([attendance_data])
    
    # Define file path for the Excel file
    file_path = 'attendance_data.xlsx'
    
    # Save to Excel file
    try:
        # If file exists, append new data
        df.to_excel(file_path, mode='a', header=False, index=False)
    except FileNotFoundError:
        # If file doesn't exist, create new file with header
        df.to_excel(file_path, index=False)
    
    # Return a success message
    return jsonify({'message': 'Attendance saved successfully!'})

if __name__ == '__main__':
    # Run the application on all addresses with port 8000
    app.run(host='0.0.0.0', port=8000)
