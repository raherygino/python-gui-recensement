from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class TableWidget(QTableWidget):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.colNoEditable = []
        self.isIncrement = False
        
    def setData(self, items):
        self.setRowCount(0)
        for row, item in enumerate(items):
            self.insertRow(row)
            for col, value in enumerate(item):
                widgetItem = QTableWidgetItem(str(value))
                self.setItem(row, col, widgetItem)
                if self.isIncrement:
                    cols = self.colNoEditable
                    if col in range(cols[0], cols[1]):
                        widgetItem.setFlags(widgetItem.flags() & ~Qt.ItemIsEditable)
                else :
                    if col in self.colNoEditable:
                        widgetItem.setFlags(widgetItem.flags() & ~Qt.ItemIsEditable)