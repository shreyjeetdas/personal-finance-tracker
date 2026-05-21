from db_connection import get_connection


def insert():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
    INSERT INTO transactions (date, amount, category, description)
    VALUES (%s, %s, %s, %s)
""",
        ("2026-08-20", 500, "Expense", "Food"),
    )
    conn.commit()
    print("Transaction inserted!")

    cur.close()
    conn.close()


def update():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE transactions
        SET amount = %s
        WHERE id = %s
    """,
        (1000, 1),
    )
    conn.commit()

    cur.close()
    conn.close()


def delete():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM transactions
        WHERE id = %s
    """,
        (1,),
    )
    conn.commit()

    cur.close()
    conn.close()


def fetch():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM transactions")
    rows = cur.fetchall()
    for row in rows:
        print(row)
        
    cur.close()
    conn.close()
