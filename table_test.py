import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor

class MyTableWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create a QVBoxLayout
        layout = QVBoxLayout()

        # Create a QTableWidget
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(4)
        self.table_widget.setColumnCount(3)

        # Add QTableWidgetItems
        for row in range(4):
            for column in range(3):
                item = QTableWidgetItem(f"Row {row + 1}, Column {column + 1}")
                self.table_widget.setItem(row, column, item)
                
                # Set background color for the item
                if column == 1:
                    item.setBackground(QColor(250, 240, 240))  # Set red background for a specific cell
                '''else:
                    item.setBackground(QColor(240, 240, 240))  # Set light gray background for all other cells'''

        # Add the table widget to the layout
        layout.addWidget(self.table_widget)

        # Set the layout to the QWidget
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyTableWidget()
    window.setWindowTitle('QTableWidget Background Example')
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())
