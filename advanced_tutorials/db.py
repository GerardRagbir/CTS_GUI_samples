import sqlite3

def first_run():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS people (id INTEGER PRIMARY KEY, name TEXT)''')
    c.execute('''ALTER TABLE tasks ADD COLUMN person_id INTEGER''')
    conn.commit()
    conn.close()
