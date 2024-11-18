import sqlite3
import console


class PinsDB():
    def __init__(self, path: str, keyword_len: int = 50):
        # Maximum length of the keyword a pin can have.
        self.keyword_len = keyword_len

        # Database variables.
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
            server_id INTEGER NOT NULL,
            channel_id INTEGER,
            message_id INTEGER,
            keyword TEXT NOT NULL,
            urls TEXT NOT NULL,
            url_count INTEGER NOT NULL
        );
        '''

        self._cursor.execute(query)
        self._conn.commit()
    
    def __del__(self):
        self.close()
    
    def close(self):
        if self._conn:
            self._conn.close()
            console.log("Successfully closed the connection with the SQLite database.")

    def add_pin(
            self,
            keyword: str,
            urls: str,
            url_count: int,
            server_id: int,
            channel_id: int = None,
            message_id: int = None
            ):
        self._cursor.execute("INSERT INTO pins VALUES (?, ?, ?, ?, ?, ?);", (server_id, channel_id, message_id, keyword, urls, url_count))
        self._conn.commit()

    # Fetch a list of all of the pins from the server.
    def get_pins_by_server_id(self, server_id: int):
        self._cursor.execute("SELECT channel_id, message_id, keyword, urls, url_count FROM pins WHERE server_id = ?;", (server_id,))
        return self._cursor.fetchall()
    
    # Fetch only the pin keywords from the server.
    def get_keywords_by_server_id(self, server_id: int):
        self._cursor.execute("SELECT keyword FROM pins WHERE server_id = ?;", (server_id,))
        return self._cursor.fetchall()

    def get_pin_by_keyword(self, server_id: int, keyword: str):
        self._cursor.execute("SELECT channel_id, message_id, urls, url_count FROM pins WHERE server_id = ? AND keyword = ?;", (server_id, keyword))
        return self._cursor.fetchall()
