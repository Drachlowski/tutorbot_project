Maximale Punkte: 2

Aufgabe:
Geben Sie alle Kunden aus, die mindestens eine Bestellung aufgegeben haben. Nutzen Sie eine Unterabfrage.

Bewertungskriterien:
Ziehe 1 Punkt ab, wenn keine Unterabfrage verwendet wurde.  
Ziehe 0.5 Punkte ab, wenn DISTINCT fehlt oder Dubletten nicht ausgeschlossen sind.

Lösung:
````sql
SELECT name
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id
    FROM orders
)
````