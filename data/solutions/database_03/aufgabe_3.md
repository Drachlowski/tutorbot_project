Maximale Punkte: 3

Aufgabe:
Ermitteln Sie für jeden Kurs die durchschnittliche Note, zeigen Sie aber nur jene Kurse an, bei denen der Schnitt unter 2,5 liegt.

Bewertungskriterien:

| Kriterium                                     | Punkte |
|-----------------------------------------------|--------|
| Richtiger Einsatz von `AVG()`                 | 0.5    |
| Richtige Verwendung von `GROUP BY`            | 0.5    |
| Richtiges Filtern mit `HAVING`                | 1.0    |
| Richtige Spalten (z. B. `course_id`, `grade`) | 0.5    |
| Gültige SQL-Syntax & lesbarer Aufbau          | 0.5    |



Lösung:
```sql
SELECT course_id, AVG(grade) AS avg_grade
FROM enrollments
GROUP BY course_id
HAVING AVG(grade) < 2.5;
```