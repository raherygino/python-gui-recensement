import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import sqlite3

class Model:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
        self.conn.commit()

    def fetch_all_items(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM items''')
        return cursor.fetchall()

    def add_item(self, name):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO items (name) VALUES (?)''', (name,))
        self.conn.commit()

    def update_item(self, item_id, new_name):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE items SET name=? WHERE id=?''', (new_name, item_id))
        self.conn.commit()

    def delete_item(self, item_id):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM items WHERE id=?''', (item_id,))
        self.conn.commit()

class Presenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.populate_table()
        self.view.show()

    def populate_table(self):
        items = self.model.fetch_all_items()
        self.view.populate_table(items)

    def add_item(self, name):
        self.model.add_item(name)
        self.populate_table()

    def update_item(self, item_id, new_name):
        self.model.update_item(item_id, new_name)
        self.populate_table()

    def delete_item(self, item_id):
        self.model.delete_item(item_id)
        self.populate_table()

class View(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_clicked)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Name"])

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_edit)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.table)

        self.central_widget.setLayout(self.layout)

    def add_clicked(self):
        name = self.name_edit.text()
        self.presenter.add_item(name)
        self.name_edit.clear()

    def populate_table(self, items):
        self.table.setRowCount(0)
        for row, item in enumerate(items):
            self.table.insertRow(row)
            for col, value in enumerate(item):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

def main():
    app = QApplication(sys.argv)
    model = Model()
    view = View()
    presenter = Presenter(view, model)
    view.presenter = presenter
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
