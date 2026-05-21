import psycopg2

conn = None
cur = None

try:
    conn = psycopg2.connect(
        host="localhost",
        database="finance_db",
        user="postgres",
        password="Papun@23",
        port="5432"
    )
    print("Connected successfully!")

    cur = conn.cursor()
    cur.execute("""
    INSERT INTO transactions (date, amount, category, description)
    VALUES (%s, %s, %s, %s)
""", ("2026-08-20", 500, "Expense", "Food"))
    conn.commit()

    print("Transaction inserted!")

except Exception as e:
    print(e)

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()


