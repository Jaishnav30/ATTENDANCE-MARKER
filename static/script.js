function submitAttendance() {
    const form = document.getElementById('attendanceForm');
    const formData = new FormData(form);

    const attendanceData = {};
    formData.forEach((value, key) => {
        attendanceData[key] = value;
    });

    // Include the date in the data sent to the server
    const dateBox = document.getElementById('dateBox');
    attendanceData['date'] = dateBox.innerText;

    fetch('/save_attendance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(attendanceData),
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {throw new Error(text)});
        }
        return response.json();
    })
    .then(data => {
        alert('Attendance saved successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while saving attendance.');
    });
}

function updateDate() {
    const dateBox = document.getElementById('dateBox');
    const today = new Date();
    
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const currentDate = today.toLocaleDateString('en-US', options);
    
    dateBox.innerText = currentDate;
}

// Call the function to set the date on page load
updateDate();
