import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("data.sqlite")


# ============================================================
# PART 1
# ============================================================

q1 = """
SELECT
    e.firstName,
    e.lastName,
    e.jobTitle
FROM employees AS e
JOIN offices AS o
    ON e.officeCode = o.officeCode
WHERE o.city = 'Boston';
"""

print("PART 1 - Employees in Boston")
print(pd.read_sql(q1, conn))


q2 = """
SELECT
    o.officeCode,
    o.city,
    COUNT(e.employeeNumber) AS n_employees
FROM offices AS o
LEFT JOIN employees AS e
    ON o.officeCode = e.officeCode
GROUP BY
    o.officeCode,
    o.city
HAVING COUNT(e.employeeNumber) = 0;
"""

print("\nPART 1 - Offices with zero employees")
print(pd.read_sql(q2, conn))


# ============================================================
# PART 2
# ============================================================

q3 = """
SELECT
    e.firstName,
    e.lastName,
    o.city,
    o.state
FROM employees AS e
LEFT JOIN offices AS o
    ON e.officeCode = o.officeCode
ORDER BY
    e.firstName,
    e.lastName;
"""

print("\nPART 2 - All employees and offices")
print(pd.read_sql(q3, conn))


q4 = """
SELECT
    c.contactFirstName,
    c.contactLastName,
    c.phone,
    c.salesRepEmployeeNumber
FROM customers AS c
LEFT JOIN orders AS ord
    ON c.customerNumber = ord.customerNumber
WHERE ord.orderNumber IS NULL
ORDER BY c.contactLastName;
"""

print("\nPART 2 - Customers with no orders")
print(pd.read_sql(q4, conn))


# ============================================================
# PART 3
# ============================================================

q5 = """
SELECT
    c.contactFirstName,
    c.contactLastName,
    p.amount,
    p.paymentDate
FROM customers AS c
JOIN payments AS p
    ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC;
"""

print("\nPART 3 - Payments")
print(pd.read_sql(q5, conn))


# ============================================================
# PART 4
# ============================================================

q6 = """
SELECT
    e.employeeNumber,
    e.firstName,
    e.lastName,
    COUNT(c.customerNumber) AS n_customers
FROM employees AS e
JOIN customers AS c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY
    e.employeeNumber,
    e.firstName,
    e.lastName
HAVING AVG(c.creditLimit) > 90000
ORDER BY n_customers DESC;
"""

print("\nPART 4 - Employees with high average customer credit")
print(pd.read_sql(q6, conn))


q7 = """
SELECT
    p.productName,
    COUNT(od.orderNumber) AS numorders,
    SUM(od.quantityOrdered) AS totalunits
FROM products AS p
JOIN orderdetails AS od
    ON p.productCode = od.productCode
GROUP BY
    p.productCode,
    p.productName
ORDER BY totalunits DESC;
"""

print("\nPART 4 - Best selling products")
print(pd.read_sql(q7, conn))


# ============================================================
# PART 5
# ============================================================

q8 = """
SELECT
    p.productName,
    p.productCode,
    COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products AS p
JOIN orderdetails AS od
    ON p.productCode = od.productCode
JOIN orders AS o
    ON od.orderNumber = o.orderNumber
GROUP BY
    p.productCode,
    p.productName
ORDER BY numpurchasers DESC;
"""

print("\nPART 5 - Product purchasers")
print(pd.read_sql(q8, conn))


q9 = """
SELECT
    COUNT(c.customerNumber) AS n_customers,
    o.officeCode,
    o.city
FROM offices AS o
LEFT JOIN employees AS e
    ON o.officeCode = e.officeCode
LEFT JOIN customers AS c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY
    o.officeCode,
    o.city
ORDER BY o.officeCode;
"""

print("\nPART 5 - Customers per office")
print(pd.read_sql(q9, conn))


# ============================================================
# PART 6
# ============================================================

q10 = """
SELECT DISTINCT
    e.employeeNumber,
    e.firstName,
    e.lastName,
    o.city,
    o.officeCode
FROM employees AS e
JOIN offices AS o
    ON e.officeCode = o.officeCode
JOIN customers AS c
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders AS ord
    ON c.customerNumber = ord.customerNumber
JOIN orderdetails AS od
    ON ord.orderNumber = od.orderNumber
WHERE od.productCode IN (
    SELECT od2.productCode
    FROM orderdetails AS od2
    JOIN orders AS ord2
        ON od2.orderNumber = ord2.orderNumber
    GROUP BY od2.productCode
    HAVING COUNT(DISTINCT ord2.customerNumber) < 20
);
"""

print("\nPART 6 - Employees who sold underperforming products")
print(pd.read_sql(q10, conn))


# Close connection
conn.close()