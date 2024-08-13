from flask import Flask, render_template, request, jsonify
from openpyxl import load_workbook
import os

app = Flask(__name__, template_folder='frontend')  # Set 'frontend' as the template folder

# Load the existing Excel workbook
workbook_path = os.path.join(os.path.dirname(__file__), 'data', 'attendance.xlsx')
workbook = load_workbook(workbook_path)
sheet = workbook.active

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_attendance', methods=['POST'])
def save_attendance():
    data = request.json
    date_day = data.pop('date')

    # Check if the date/day already exists in the sheet
    date_column = None
    for col in range(3, sheet.max_column + 1):
        if sheet.cell(row=1, column=col).value == date_day:
            date_column = col
            break

    if (date_column is None):
        date_column = sheet.max_column + 1
        sheet.cell(row=1, column=date_column).value = date_day

    # Iterate over the attendance data to update the Excel sheet
    for student, attendance in data.items():
        for row in range(2, sheet.max_row + 1):
            if sheet.cell(row=row, column=2).value == student:
                sheet.cell(row=row, column=date_column).value = attendance
                break

    # Save the updated workbook
    workbook.save(workbook_path)

    return jsonify({'message': 'Attendance saved successfully!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
