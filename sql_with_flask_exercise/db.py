import psycopg2


def connect():
    c = psycopg2.connect("dbname=flask-sql-snacks user=timo")
    return c


def get_all_snacks():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM snacks")
    toys = cur.fetchall()
    cur.close()
    conn.close()
    return toys


def add_snack(name, kind):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO snacks (name, kind) VALUES (%s, %s)", (name, kind))
    conn.commit()
    cur.close()
    conn.close()


def update_snack(id, name, kind):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE snacks SET name = (%s), kind = (%s) WHERE id = (%s)", (name, kind, id))
    conn.commit()
    cur.close()
    conn.close()


def delete_snack(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM snacks WHERE id = (%s)", (id,))
    conn.commit()
    cur.close()
    conn.close()
