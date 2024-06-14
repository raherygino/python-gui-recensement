from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reinitialize QTableWidget Data")

        # Create a table widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])

        # Fill initial data
        self.fill_table_data()

        # Create a button to reinitialize data
        self.reinitialize_button = QPushButton("Reinitialize Data")
        self.reinitialize_button.clicked.connect(self.reinitialize_data)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.reinitialize_button)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def fill_table_data(self):
        # Fill the table with initial data
        data = [
            ("Row 1", "Value 1", "Value 2"),
            ("Row 2", "Value 3", "Value 4"),
            ("Row 3", "Value 5", "Value 6")
        ]

        self.tableWidget.setRowCount(len(data))

        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                item = QTableWidgetItem(value)
                self.tableWidget.setItem(row, col, item)

    def reinitialize_data(self):
        # Clear existing data
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        # Refill with new data
        self.fill_table_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
