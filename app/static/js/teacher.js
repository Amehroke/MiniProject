const url1 = 'http://127.0.0.1:5000/courses';
const main = document.querySelector("main");

// Function to display courses, assuming data is passed correctly
function displayCourses(data) {
    main.innerHTML = ''; // Clear the main element before displaying results

    // Create table and headers
    const table = document.createElement('table');
    table.classList.add('table', 'table-striped');
    table.innerHTML = `
        <thead>
            <tr>
                <th>Course Name</th>
                <th>Teacher</th>
                <th>Time</th>
                <th>Students Enrolled</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    `;

    // Append table to main
    main.append(table);
    const tbody = table.querySelector('tbody');

    // Loop through data to create rows for each course
    data.forEach(course => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${course.name}</td>
            <td>${course.teacher}</td>
            <td>${course.time}</td>
            <td>${course.capacity}</td>
        `;
        tbody.append(tr);
    });
}

// Define an async function to fetch courses
async function fetchCourses(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const courses = await response.json();
        displayCourses(courses);
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
    }
}

// Call fetchCourses to initially load all courses
fetchCourses(url1);
