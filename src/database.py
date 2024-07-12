import sqlite3
import console


class Database():
    def __init__(self, path: str):
        self._conn: sqlite3.Connection = None
        self._cursor: sqlite3.Cursor = None

        # Connect to the database, or create one if it doesn't exist.
        try:
            self._conn = sqlite3.connect(path)
            self._cursor = self._conn.cursor()
            console.log("Successfully connected to a SQLite database.")
        except Exception as e:
            console.log("Couldn't connect to a SQLite database.", console.Level.CRITICAL)
            self.close()

        # Create a table where we'll save pins, if it doesn't already exist.
        query = '''
        CREATE TABLE IF NOT EXISTS pins(
            server_id TEXT NOT NULL,
            name TEXT NOT NULL,
            url TEXT NOT NULL
        );
        '''

        self._cursor.execute(query)
        self._conn.commit()
    

    def close(self):
        if self._conn:
            self._conn.close()
            console.log("Successfully closed the connection with the SQLite database.")


    def insert_pin(self, server_id, name, url):
        self._cursor.execute("INSERT INTO pins VALUES (?, ?, ?);", (server_id, name, url))
        self._conn.commit()


    def get_pins_by_server_id(self, server_id):
        self._cursor.execute("SELECT name, url FROM pins WHERE server_id = ?;", (server_id,))
        return self._cursor.fetchall()


    def get_pin_by_name(self, server_id, name):
        self._cursor.execute("SELECT name, url FROM pins WHERE server_id = ? AND name = ?;", (server_id, name))
        return self._cursor.fetchall()
