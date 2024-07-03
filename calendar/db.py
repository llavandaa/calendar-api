import sqlite3
from model import Event

class Database:
    def __init__(self, db_name='calendar.db'):
        self.connection = sqlite3.connect(db_name)
        self._create_table()

    def _create_table(self):
        with self.connection:
            self.connection.execute(
                '''CREATE TABLE IF NOT EXISTS events (
                    id TEXT PRIMARY KEY,
                    date TEXT NOT NULL,
                    title TEXT NOT NULL,
                    text TEXT NOT NULL
                )'''
            )

    def insert(self, event):
        with self.connection:
            self.connection.execute(
                "INSERT INTO events (id, date, title, text) VALUES (?, ?, ?, ?)",
                (event.id, event.date, event.title, event.text)
            )

    def select_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, date, title, text FROM events")
        rows = cursor.fetchall()
        events = []
        for row in rows:
            event = Event()
            event.id, event.date, event.title, event.text = row
            events.append(event)
        return events

    def select(self, _id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, date, title, text FROM events WHERE id = ?", (_id,))
        row = cursor.fetchone()
        if row:
            event = Event()
            event.id, event.date, event.title, event.text = row
            return event
        return None

    def update(self, event):
        with self.connection:
            self.connection.execute(
                "UPDATE events SET date = ?, title = ?, text = ? WHERE id = ?",
                (event.date, event.title, event.text, event.id)
            )

    def delete(self, _id):
        with self.connection:
            self.connection.execute("DELETE FROM events WHERE id = ?", (_id,))
