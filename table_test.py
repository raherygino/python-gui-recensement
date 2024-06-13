from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
import sys

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'Age'])

        self.tableWidget.setItem(0, 0, QTableWidgetItem('John'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('30'))
        self.tableWidget.setItem(1, 0, QTableWidgetItem('Alice'))
        self.tableWidget.setItem(1, 1, QTableWidgetItem('25'))
        self.tableWidget.setItem(2, 0, QTableWidgetItem('Bob'))
        self.tableWidget.setItem(2, 1, QTableWidgetItem('35'))

        self.button = QPushButton('Reset Table')
        self.button.clicked.connect(self.reset_table)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def reset_table(self):
        self.tableWidget.clear()  # Clear all data
        self.tableWidget.setRowCount(2)  # Reset row count
        self.tableWidget.setColumnCount(0)  # Reset column count
        new_headers = ['New Header 1', 'New Header 2']  # New headers
        self.tableWidget.setColumnCount(len(new_headers))
        self.tableWidget.setHorizontalHeaderLabels(new_headers)
        self.tableWidget.setItem(0, 0, QTableWidgetItem('John'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('30'))
        self.tableWidget.setItem(1, 0, QTableWidgetItem('Alice'))
        self.tableWidget.setItem(1, 1, QTableWidgetItem('25'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
