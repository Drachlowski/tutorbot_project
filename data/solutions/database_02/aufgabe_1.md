Maximale Punkte: 2

Aufgabe:
Geben Sie alle Kundennamen aus der Tabelle customers aus, die in der Stadt "Linz" wohnen.

Bewertungskriterien:
Ziehe 0.5 Punkte ab, wenn Spaltennamen nicht korrekt oder unvollständig angegeben wurden. Es darf nur "name" selektiert werden.
Ziehe 1 Punkt ab, wenn kein WHERE-Filter auf city verwendet wurde.

Lösung:
````sql
SELECT name
FROM customers
WHERE city = 'Linz'
````