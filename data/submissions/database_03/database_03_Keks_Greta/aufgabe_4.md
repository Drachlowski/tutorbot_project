SELECT students.name AS student_name, courses.name AS course_name
FROM students
JOIN enrollments ON students.id = enrollments.student_id
JOIN courses ON enrollments.course_id = courses.id
ORDER BY students.name;
