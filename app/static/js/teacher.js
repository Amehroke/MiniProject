
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.view-grades').forEach(button => {
        button.addEventListener('click', function() {
            var courseId = this.getAttribute('data-course-id');
            // Redirect to a grade editing page or open a modal
            window.location.href = `/edit-grades?courseId=${courseId}`;
        });
    });
});

