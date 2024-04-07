const url = 'http://127.0.0.1:5000/grade'; 


//Add New Student
async function addStudentGrade(studentName, grade) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: studentName, grade: grade }),
            
        });
        if (!response.ok) {
            if (response.status === 409) {
                alert("This student already exists. Please update the existing student grade or add a different student.");
            } else {
                throw new Error(`Network response was not ok (${response.status})`);
            }
        }

        alert("Student Added Successfully");

        document.getElementById('s_name').value = '';
        document.getElementById('s_grade').value = '';

    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
    }
    
    route
}



document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('add-student-form').addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission

        const studentName = document.getElementById('s_name').value;
        const studentGrade = document.getElementById('s_grade').value;

        if (studentName && studentGrade) {
            addStudentGrade(studentName, studentGrade);
        } else {
            alert("Please fill in all fields.");
        }
    });
});
