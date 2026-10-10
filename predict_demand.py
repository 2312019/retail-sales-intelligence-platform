import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import joblib

model = joblib.load("model.pkl")
product_mapping = joblib.load("product_mapping.pkl")

reverse_mapping = {v: k for k, v in product_mapping.items()}

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harish-73",
    database="mcpp_db"
)

cursor = conn.cursor()

future_date = datetime.now().date() + timedelta(days=1)

day = future_date.day
month = future_date.month
year = future_date.year
weekday = future_date.weekday()

cursor.execute("DELETE FROM predicted_demand WHERE prediction_date = %s", (future_date,))
conn.commit()

cursor.execute("SELECT product_id FROM products")
products = cursor.fetchall()

for row in products:
    product_id = str(row[0])

    if product_id not in reverse_mapping:
        continue

    product_code = reverse_mapping[product_id]

    future_data = pd.DataFrame({
        'product_code': [product_code],
        'day': [day],
        'month': [month],
        'year': [year],
        'weekday': [weekday]
    })

    predicted_qty = float(model.predict(future_data)[0])

    cursor.execute("""
        INSERT INTO predicted_demand (product_id, prediction_date, predicted_quantity)
        VALUES (%s, %s, %s)
    """, (product_id, future_date, predicted_qty))

conn.commit()
cursor.close()
conn.close()

print("✅ Predictions inserted successfully!")