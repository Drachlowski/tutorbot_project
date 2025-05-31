SELECT l.name AS lecturer_name, COUNT(DISTINCT e.student_id) AS student_count
FROM lecturers l
JOIN courses c ON l.id = c.lecturer_id
JOIN enrollments e ON c.id = e.course_id
GROUP BY l.name
HAVING COUNT(DISTINCT e.student_id) > 10;
