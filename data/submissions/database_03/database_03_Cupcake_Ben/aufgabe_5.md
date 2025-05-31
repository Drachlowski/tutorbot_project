SELECT s.name, c.name 
FROM students s, enrollments e, courses c 
WHERE s.id = e.student_id AND e.course_id = c.id;
