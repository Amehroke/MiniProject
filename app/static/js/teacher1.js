const url1 = 'http://127.0.0.1:5000/courses'; 
const main = document.querySelector("main");

{/* <div class="row">
            <div class="col-md-12">
                <h2>Your Courses</h2>
                
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Course Name</th>
                            <th>Teacher</th>
                            <th>Time</th>
                            <th>Students Enrolled</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for course in courses %}
                            <tr>
                                <td>{{ Class.name }}</td>
                                <td>{{ course.code }}</td>
                                <td>{{ course.students.count() }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div> */}

// Function to display students
function displayCourses(data) {
    main.innerHTML = ''; // Clear the main element before displaying results
    for (student in data) {
        let gradeArticle = document.createElement('article');
        gradeArticle.classList.add('grade');
        gradeArticle.setAttribute('data-id', student);

        gradeArticle.innerHTML = `
            <button class="delete-btn" data-student= "${student}" >X</button>
            <h3 class="student_name">Student Name: ${student}</h3>
            <p class="student_grade">Grade: ${data[student]}</p>
            <button class="upd-btn" data-student="${student}">Update</button>
        `;

        main.append(gradeArticle);
    }

    // // Add event listeners for delete button
    // document.querySelectorAll('.delete-btn').forEach(button => {
    //     button.addEventListener('click', function() {

    //         const studentName = this.getAttribute('data-student');
    //         // Confirmation dialog
    //         const userConfirmed = confirm(`Are you sure you want to delete ${studentName}?`);
            
    //         if (userConfirmed) {
    //             deleteStudentGrade(studentName);
    //         }
    //         // If the user clicks "Cancel", nothing happens thanks to the if condition
    //     });
    // });

    // document.querySelectorAll('.upd-btn').forEach(button => {
    //     button.addEventListener('click', function() {
    //         const studentName = this.getAttribute('data-student');
    //         const newGrade = prompt(`Enter new grade for ${studentName}:`);

    //         // Basic validation for grade input
    //         if (newGrade !== null && newGrade.trim() !== "" && !isNaN(newGrade) && parseInt(newGrade) >= 0) {
    //             updateStudentGrade(studentName, parseInt(newGrade));
    //         } else if (newGrade !== null) { // Ensure prompt was not cancelled
    //             alert("Invalid grade input. Please enter a numeric value.");
    //         }
    //     });
    // });

}


// Define an async function to fetch grades
async function fetchGrades(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        displayStudents(data);
    } catch (error) {
        console.log('There was a problem with your fetch operation:', error);
    }
}

//getGrades
async function fetchStudentGrades(studentName) {
    const url = `http://127.0.0.1:5000/grade/${encodeURIComponent(studentName)}`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            alert("Student not found");
            throw new Error(`Network response was not ok (${response.status})`);
        }
        const data = await response.json();
        displayStudents(data);
    } catch (error) {
        console.error('url', error);
    }
}


//Update Student Grade
async function updateStudentGrade(studentName, newGrade) {
    const url = `http://127.0.0.1:5000/grade/${encodeURIComponent(studentName)}`;
    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ grade: newGrade }),
        });
        if (!response.ok) {
            throw new Error(`Network response was not ok (${response.status})`);
        }
        const data = await response.json();
        console.log('Updated grade:', data); // For debugging
        fetchGrades(url1); // Refresh the list after update
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
    }
}



//Delete Student grade
async function deleteStudentGrade(studentName) {
    const url = `http://127.0.0.1:5000/grade/${encodeURIComponent(studentName)}`;
    try {
        const response = await fetch(url, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error(`Network response was not ok (${response.status})`);
        }
        const data = await response.json();
        displayStudents(data);
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
    }
    fetchGrades(url1);
}

// Correct initial fetch call
fetchGrades(url1); // Call this to initially load all grades

