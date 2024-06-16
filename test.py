from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fixed Row Example")
        self.setGeometry(100, 100, 600, 400)

        # Create a table widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(3)

        # Populate the table with some data
        for row in range(5):
            for col in range(3):
                item = QTableWidgetItem(f"Row {row} Col {col}")
                self.tableWidget.setItem(row, col, item)

        # Make the first row read-only (fixed)
        for col in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(0, col)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        # Create a central widget
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
