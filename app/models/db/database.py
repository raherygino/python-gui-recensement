import sqlite3
import os

class Database():
    def connect(self):
        folder_path = os.path.expanduser("~/AppData/Local/gdc/")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return sqlite3.connect(f"database.db")