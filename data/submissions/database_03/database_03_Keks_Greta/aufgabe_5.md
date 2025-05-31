SELECT lecturers.name AS lecturer_name, COUNT(DISTINCT enrollments.student_id) AS student_count
FROM lecturers
JOIN courses ON lecturers.id = courses.lecturer_id
JOIN enrollments ON courses.id = enrollments.course_id
GROUP BY lecturers.name
HAVING COUNT(DISTINCT enrollments.student_id) > 10;
