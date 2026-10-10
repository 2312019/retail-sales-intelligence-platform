import mysql.connector
import random
import time
from datetime import datetime, timedelta

# 🔹 DATABASE CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harish-73",
    database="mcpp_db"
)

cursor = conn.cursor()

print("🚀 Retail Sales Generator Started...")

# ==================================================
# 🟡 STEP 1: CHECK IF DATA ALREADY EXISTS
# ==================================================

cursor.execute("SELECT COUNT(*) FROM sales")
count = cursor.fetchone()[0]

# ==================================================
# 🟡 STEP 2: INSERT FULL-YEAR PAST DATA (ONLY FIRST TIME)
# ==================================================

if count == 0:
    print("📅 Generating full-year past sales data...")

    start_date = datetime(2026, 1, 1)

    for i in range(300):   # 300 past sales across full year

        cursor.execute("SELECT product_id, price FROM products ORDER BY RAND() LIMIT 1")
        product_id, price = cursor.fetchone()

        cursor.execute("SELECT customer_id FROM customers ORDER BY RAND() LIMIT 1")
        customer_id = cursor.fetchone()[0]

        quantity = random.randint(1, 5)
        total = price * quantity

        # random date and time across full year
        random_dt = start_date + timedelta(
            days=random.randint(0, 364),
            hours=random.randint(8, 22),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        query = """
        INSERT INTO sales 
        (product_id, customer_id, quantity, total_amount, sale_date, sale_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            product_id,
            customer_id,
            quantity,
            total,
            random_dt.date(),
            random_dt.time()
        ))

    conn.commit()
    print("✅ Full-year past data inserted!")

else:
    print("ℹ️ Data already exists, skipping past data...")

# ==================================================
# 🟢 STEP 3: REAL-TIME DATA (RUN CONTINUOUSLY)
# ==================================================

print("🔴 Real-time sales started... (Press CTRL+C to stop)")

while True:
    try:
        cursor.execute("SELECT product_id, price FROM products ORDER BY RAND() LIMIT 1")
        product_id, price = cursor.fetchone()

        cursor.execute("SELECT customer_id FROM customers ORDER BY RAND() LIMIT 1")
        customer_id = cursor.fetchone()[0]

        quantity = random.randint(1, 5)
        total = price * quantity

        now = datetime.now()

        query = """
        INSERT INTO sales 
        (product_id, customer_id, quantity, total_amount, sale_date, sale_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            product_id,
            customer_id,
            quantity,
            total,
            now.date(),
            now.time()
        ))

        conn.commit()

        print(f"🟢 New Sale → {product_id} | {customer_id} | ₹{total}")

        time.sleep(5)   # every 5 seconds

    except KeyboardInterrupt:
        print("\n⛔ Stopped by user")
        break

# 🔹 CLOSE CONNECTION
cursor.close()
conn.close()