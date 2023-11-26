SELECT Exc_date, Currency, Exc_rate
FROM rates
WHERE Exc_date >= (SELECT DATE(MAX(Exc_date), '-90 day')
FROM rates)