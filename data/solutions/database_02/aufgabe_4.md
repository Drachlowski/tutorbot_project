Maximale Punkte: 2

Aufgabe:
Zählen Sie, wie viele Bestellungen es insgesamt in der Tabelle orders gibt.

Bewertungskriterien:
Ziehe 1 Punkt ab, wenn kein COUNT(*) verwendet wurde.  
Ziehe 0.5 Punkte ab, wenn das Ergebnis nicht mit einem Alias versehen ist.

Lösung:
````sql
SELECT COUNT(*) AS total_orders
FROM orders
````