from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Path to your Excel file
EXCEL_FILE = 'attendance.xlsx'

def read_excel():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE, sheet_name=None)
    else:
        # Create a new DataFrame with headers if file doesn't exist
        df = pd.DataFrame(columns=['USN', 'Student Name'])
        return {'Sheet1': df}

def save_to_excel(data):
    df = read_excel()
    sheet_name = 'Sheet1'
    
    # Check if the sheet already exists
    if sheet_name not in df:
        df[sheet_name] = pd.DataFrame(columns=['USN', 'Student Name'])
    
    # Convert attendance data into DataFrame
    attendance_df = pd.DataFrame(data)
    
    # Ensure 'date' column exists in DataFrame
    if 'date' not in attendance_df.columns:
        return "Date column is missing in the data", 400
    
    date_col = attendance_df['date'].iloc[0]
    
    # Update existing data or add new columns
    if date_col not in df[sheet_name].columns:
        df[sheet_name][date_col] = None

    # Update attendance data
    for index, row in attendance_df.iterrows():
        student_name = row['Student Name']
        presence = row[date_col]
        if student_name in df[sheet_name]['Student Name'].values:
            df[sheet_name].loc[df[sheet_name]['Student Name'] == student_name, date_col] = presence
        else:
            df[sheet_name] = df[sheet_name].append({'USN': row['USN'], 'Student Name': student_name, date_col: presence}, ignore_index=True)
    
    # Save to Excel file
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
        for sheet, sheet_df in df.items():
            sheet_df.to_excel(writer, sheet_name=sheet, index=False)

@app.route('/save_attendance', methods=['POST'])
def save_attendance():
    data = request.json
    
    # Validate received data
    if 'date' not in data:
        return "Date not provided", 400
    
    # Save to Excel
    save_to_excel(data)
    
    return jsonify({"message": "Attendance saved successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
