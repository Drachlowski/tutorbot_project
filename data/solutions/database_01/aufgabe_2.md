Maximale Punkte: 2

Aufgabe:
Geben Sie alle Kundennamen aus der Tabelle customers aus, die in der Stadt "Linz" wohnen.

Bewertungskriterien:
Ziehe 0.5 Punkte ab, wenn mehr Spalten, als nur der Name selektiert werden.
Ziehe 1 Punkt ab, wenn nicht dokumentiert wurde, wie man die Stadt herausfiltert.

Lösung:
````sql
SELECT name
FROM customers
WHERE city = 'Linz'
````