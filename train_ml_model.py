import pandas as pd
import mysql.connector
from sklearn.ensemble import RandomForestRegressor
import joblib

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harish-73",
    database="mcpp_db"
)

query = """
SELECT 
    product_id,
    sale_date,
    SUM(quantity) AS total_qty
FROM sales
GROUP BY product_id, sale_date
ORDER BY product_id, sale_date
"""

df = pd.read_sql(query, conn)
conn.close()

df['sale_date'] = pd.to_datetime(df['sale_date'])
df['day'] = df['sale_date'].dt.day
df['month'] = df['sale_date'].dt.month
df['year'] = df['sale_date'].dt.year
df['weekday'] = df['sale_date'].dt.weekday

df['product_id'] = df['product_id'].astype(str)
df['product_code'] = df['product_id'].astype('category').cat.codes

product_mapping = dict(enumerate(df['product_id'].astype('category').cat.categories))
joblib.dump(product_mapping, "product_mapping.pkl")

X = df[['product_code', 'day', 'month', 'year', 'weekday']]
y = df['total_qty']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, "model.pkl")
print("✅ ML Model Trained & Saved")
print("✅ Product mapping saved")