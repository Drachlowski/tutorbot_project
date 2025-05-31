SELECT lecturers.name, COUNT(DISTINCT student_id) 
FROM lecturers 
JOIN courses ON lecturers.id = courses.lecturer_id 
JOIN enrollments ON courses.id = enrollments.course_id 
GROUP BY lecturers.name;
