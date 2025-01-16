import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

table_schema = """
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_score INTEGER NOT NULL,
    ai_score INTEGER NOT NULL
);
"""
cursor.execute(table_schema)

connection.commit()
connection.close()