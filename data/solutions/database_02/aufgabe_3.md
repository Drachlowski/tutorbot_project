Maximale Punkte: 2

Aufgabe:
Geben Sie den Namen und die Bestellnummer aller Kunden aus, indem Sie die Tabellen customers und orders verknüpfen.

Bewertungskriterien:
Ziehe 1 Punkt ab, wenn kein JOIN verwendet wurde.  
Ziehe 0.5 Punkte ab, wenn keine sprechenden Aliase verwendet wurden.

Lösung:
```sql
SELECT c.name, o.order_id
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
```