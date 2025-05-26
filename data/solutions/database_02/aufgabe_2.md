Maximale Punkte: 2

Aufgabe:
Listen Sie alle Produktnamen und deren Preise aus der Tabelle products auf, deren Preis über 50€ liegt.

Bewertungskriterien (an diese musst du dich halten):
Ziehe 1 Punkt ab, wenn die WHERE-Klausel fehlt oder falsch ist.
Ziehe 0.5 Punkte ab, wenn Spaltennamen nicht korrekt oder unvollständig angegeben wurden.

Lösung:
```sql
SELECT product_name, price
FROM products
WHERE price > 50
```