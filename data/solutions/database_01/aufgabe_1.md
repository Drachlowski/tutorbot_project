Maximale Punkte: 2

Aufgabe:
Selektieren Sie alle Spalten in der Tabelle Users

Bewertungskriterien:
Es sollen alle Spalten einzeln ausgewählt werden und nicht mit SELECT *

Lösung:
````sql
SELECT
    ID,
    VORNAME,
    NACHNAME,
    GEBURTSDATUM
FROM
    Users
````