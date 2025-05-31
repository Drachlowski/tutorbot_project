SELECT course_id, AVG(grade) AS avg_grade
FROM enrollments
GROUP BY course_id
HAVING AVG(grade) < 2.5;
