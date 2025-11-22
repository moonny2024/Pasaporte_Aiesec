import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    fullname TEXT,
    role TEXT CHECK(role IN ('admin', 'user'))
)
""")

conn.execute("""
CREATE TABLE badges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    image TEXT,
    date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.execute("INSERT INTO users (email, password, fullname, role)" \
"VALUES ('admin@mxp.com','admin','Administrador','admin')")
conn.execute("INSERT INTO users (email, password, fullname, role)" \
"VALUES ('user@mxp.com','user','Usuario','user')")
conn.commit()
conn.close()

print("DB creada.")
