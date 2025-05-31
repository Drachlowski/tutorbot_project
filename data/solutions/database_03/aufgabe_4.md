Maximale Punkte: 4

Aufgabe:
Selektieren Sie den Namen von jedem Studierenden und den Namen der Kurse, die sie besuchen. Sortieren Sie diese nach dem Namen des Studierenden.

Bewertungskriterien:

| Kriterium                                              | Punkte |
|--------------------------------------------------------|--------|
| Korrekte Joins: `students` – `enrollments` – `courses` | 1.5    |
| Richtige Spaltenauswahl und Aliase                     | 0.5    |
| Sortierung mit `ORDER BY` korrekt angewendet           | 0.5    |
| Richtige SQL-Syntax, Klarheit & Struktur               | 0.5    |
| Kein `SELECT *`, sondern gezielte Projektion           | 0.5    |
| Tabelle & Bedingungen korrekt                          | 0.5    |


Lösung:
```sql
SELECT s.name AS student_name, c.name AS course_name
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id
ORDER BY s.name;
```