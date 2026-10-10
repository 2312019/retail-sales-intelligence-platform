import mysql.connector
from datetime import datetime

# Connect MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harish-73",
    database="mcpp_db"
)

cursor = conn.cursor(dictionary=True)

# Clean old alerts (optional)
#cursor.execute("DELETE FROM stock_alerts")
conn.commit()

# Get one prediction per product
query = """
SELECT 
    p.product_id,
    p.product_name,
    p.stock_quantity,
    MAX(d.predicted_quantity) AS predicted_quantity
FROM products p
JOIN predicted_demand d
    ON p.product_id = d.product_id
GROUP BY p.product_id, p.product_name, p.stock_quantity
"""

cursor.execute(query)
rows = cursor.fetchall()

for row in rows:
    product_id = row["product_id"]
    product_name = row["product_name"]
    stock_quantity = row["stock_quantity"]
    predicted_quantity = row["predicted_quantity"]

    if stock_quantity < 120 and predicted_quantity > 3:
        alert_message = (
            f"ALERT: {product_name} is low in stock "
            f"({stock_quantity}) and predicted demand is high "
            f"({predicted_quantity:.2f})"
        )

        print(alert_message)

        insert_query = """
        INSERT INTO stock_alerts (product_id, alert_message, alert_date)
        VALUES (%s, %s, %s)
        """

        cursor.execute(insert_query, (
            product_id,
            alert_message,
            datetime.now()
        ))

conn.commit()
cursor.close()
conn.close()

print("Alerts checked and saved successfully.")
