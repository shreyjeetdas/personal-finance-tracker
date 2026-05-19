import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="finance_db",
    user="postgres",
    password="Papun@23",
    port="5432"
)

print("Connected successfully!")

conn.close()
