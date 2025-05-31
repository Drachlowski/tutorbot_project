SELECT l.name, COUNT(e.student_id) AS student_count
FROM lecturers l
JOIN courses c ON l.id = c.lecturer_id
JOIN enrollments e ON c.id = e.course_id
GROUP BY l.name
HAVING COUNT(e.student_id) > 10;
