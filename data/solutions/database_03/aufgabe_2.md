Maximale Punkte: 2

Aufgabe:
Finde Sie alle Kurse, deren Name mit "Daten" beginnt.


Bewertungskriterien:

| Kriterium                            | Punkte |
|--------------------------------------|--------|
| Richtige Verwendung von `LIKE`       | 0.5    |
| Richtige Spalte(n) selektiert        | 0.5    |
| Richtige Tabelle                     | 0.5    |
| Gültige SQL-Syntax & sinnvoller Stil | 0.5    |


Lösung:
```sql
SELECT * FROM courses WHERE name LIKE 'Daten%';
```