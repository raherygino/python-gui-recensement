from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import sys

class MyTableWidget(QTableWidget):
    def __init__(self, rows, columns, parent=None):
        super().__init__(rows, columns, parent)
        self.setSortingEnabled(True)  # Enable sorting for the entire table

    # Implement custom sorting for a specific column
    def sortItems(self, column, order):
        if column == 1:  # Sort only if the column index is 1 (adjust this based on your column index)
            super().sortItems(column, order)
        else:
            pass  # Ignore sorting for other columns

def main():
    app = QApplication(sys.argv)
    table = MyTableWidget(5, 3)
    
    # Populate the table with some data
    for row in range(5):
        for col in range(3):
            item = QTableWidgetItem(f"Item {row},{col}")
            table.setItem(row, col, item)
            
    table.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
    
    # Show the table
    table.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
  