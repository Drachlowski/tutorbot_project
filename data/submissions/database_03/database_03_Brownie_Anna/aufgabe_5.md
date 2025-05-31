SELECT lecturer_name, COUNT(*) 
FROM lecturers 
JOIN courses 
GROUP BY lecturer;
