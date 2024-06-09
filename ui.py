import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt

class TableWidgetDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTableWidget Example")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])

        # Adding some data to the table
        data = [
            ["Editable 1", "Read-only 1", "Editable 2"],
            ["Read-only 2", "Editable 3", "Read-only 3"],
            ["Editable 4", "Read-only 4", "Editable 5"],
            ["Read-only 5", "Editable 6", "Read-only 6"]
        ]

        for row in range(len(data)):
            for column in range(len(data[row])):
                item = QTableWidgetItem(data[row][column])
                # Set editable or not based on the content (for demonstration purposes)
                if "Editable" in data[row][column]:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.tableWidget.setItem(row, column, item)

        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = TableWidgetDemo()
    demo.show()
    sys.exit(app.exec_())
