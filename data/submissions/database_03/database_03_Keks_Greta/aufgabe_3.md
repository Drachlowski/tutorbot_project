SELECT course_id, AVG(grade)
FROM enrollments
GROUP BY course_id
HAVING AVG(grade) < 2.5;
