import sqlite3
import os

class Database():
    def connect(self):
        return sqlite3.connect("database.db")