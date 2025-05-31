Maximale Punkte: 5

Aufgabe:
Gegeben sind folgende Tabellen:
- students(id, name, study_program)
- enrollments(student_id, course_id, grade)
- courses(id, name, lecturer_id)
- lecturers(id, name)

Zeigen Sie für jede unterrichtende Person, wie viele verschiedene Studierende sie in ihren Kursen unterrichtet hat, aber nur, wenn es mehr als 10 Studierende waren.

Bewertungskriterien:

| Kriterium                                                  | Punkte |
|------------------------------------------------------------|--------|
| Richtige Verknüpfung aller 4 Tabellen (3 Joins)            | 2.0    |
| Aggregation mit `COUNT(DISTINCT student_id)`               | 0.5    |
| Gruppierung nach Dozent (`GROUP BY l.name`)                | 0.5    |
| Filterung über `HAVING` > 10 korrekt angewandt             | 0.5    |
| Korrekte Ausgabe mit sinnvollen Aliassen (`lecturer_name`) | 0.5    |
| Sauberer SQL-Stil und syntaktisch korrekt                  | 1.0    |


Lösung:
```sql
SELECT l.name AS lecturer_name, COUNT(DISTINCT e.student_id) AS student_count
FROM lecturers l
JOIN courses c ON l.id = c.lecturer_id
JOIN enrollments e ON c.id = e.course_id
GROUP BY l.name
HAVING COUNT(DISTINCT e.student_id) > 10;
```