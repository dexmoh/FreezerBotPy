# This script converts the old pins text files into one single SQL database.

import os
import glob
import sqlite3


# Path to the old pins directory.
OLD_PINS_DIR: str = ".old_data/servers"

# Path to where we want to write the output file.
OUTPUT_DB_PATH: str = ".data/pins.db"


def main():
    # Create and connect to a SQL database.
    conn: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None

    try:
        conn = sqlite3.connect(OUTPUT_DB_PATH)
        cursor = conn.cursor()
        print("Successfully connected to a SQLite database.")
    except Exception as e:
        print("ERROR: Couldn't connect to a SQLite database.")
        if conn:
            conn.close()
        return

    # Create a table where we'll save pins, if it doesn't already exist.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pins(
        server_id INTEGER NOT NULL,
        channel_id INTEGER,
        message_id INTEGER,
        keyword TEXT NOT NULL,
        urls TEXT NOT NULL,
        url_count INTEGER NOT NULL
    );
    ''')
    conn.commit()

    # Iterate through the server directories and read pins.txt files.
    for folder_path in glob.glob(f"{OLD_PINS_DIR}/*"):
        # Get the server ID from the folder name.
        server_id = int(os.path.basename(folder_path))

        # Read the pins file.
        pins_file_path = os.path.join(folder_path, "pins.txt")

        with open(pins_file_path, "r", encoding="utf-8") as pins:
            keywords = []
            urls = []
            for line_num, line in enumerate(pins):
                if line_num % 2 == 0:
                    keywords.append(line.strip())
                else:
                    urls.append(line.strip())
            
            for index, keyword in enumerate(keywords):
                url_count = len(urls[index].split())

                # Insert a new pin.
                cursor.execute("INSERT INTO pins VALUES (?, NULL, NULL, ?, ?, ?);", (server_id, keyword, urls[index], url_count))
                conn.commit()

    if conn:
        conn.close()
    
    print("Done!")


if __name__ == "__main__":
    main()
