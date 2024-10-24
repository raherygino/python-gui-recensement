from typing import Iterable
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor
from ..common.config import cfg
import darkdetect

class TableView(QTableWidget):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWordWrap(False)
        self.header = self.horizontalHeader()
        self.verticalHeader().hide()
        self.setContentsMargins(0,0,0,0)
        self.setQss(cfg.get(cfg.theme))
        self.colNoEditable = []
        self.isIncrement = False
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        #self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
    def setHorizontalHeaderLabels(self, labels: Iterable[str | None]) -> None:
        self.setColumnCount(len(labels))
        return super().setHorizontalHeaderLabels(labels)
    
    def getHeaderLabels(self):
        header_labels = []
        for column in range(self.columnCount()):
            header_item = self.horizontalHeaderItem(column)
            if header_item is not None:
                header_labels.append(header_item.text())
            else:
                header_labels.append(f"Column {column}")  # Default label if item is None
        return header_labels
    
    @pyqtSlot(QTableWidgetItem)
    def validateInput(self, col, item, default = "0"):
        if item.column() == col:  # Assuming the column where you want to enforce integer input is column 1
            text = item.text()
            try:
                value = int(text)
            except ValueError:
                # If the input is not a valid integer, set it to 0 or whatever default value you prefer
                item.setText(default)
            else:
                # If the input is a valid integer, set it to the validated integer
                item.setText(str(value))
    
    def setQss(self, newTheme: str):
        theme = newTheme.lower()
        themeColor = f'rgba{str(cfg.get(cfg.themeColor).getRgb())}'
        if theme == "auto":
            theme = "light" if darkdetect.isLight() else "dark"
        with open(f'app/resource/qss/{theme}/table_view.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read().replace("#327bcc", themeColor))
        
    def setData(self, items):
        self.setRowCount(0)
        for row, item in enumerate(items):
            self.insertRow(row)
            for col, value in enumerate(item):
                widgetItem = QTableWidgetItem(str(value) if value != None else "")
                self.setItem(row, col, widgetItem)
                if self.isIncrement:
                    cols = self.colNoEditable
                    if col in range(cols[0], cols[1]):
                        widgetItem.setFlags(widgetItem.flags() & ~Qt.ItemIsEditable)
                else :
                    if col in self.colNoEditable:
                        widgetItem.setFlags(widgetItem.flags() & ~Qt.ItemIsEditable)
                
        self.resizeColumnsToContents()
        self.horizontalHeaderItem(0).setBackground(QColor(154,150,144))
        
    def setColumnNoEditable(self, *args):
        self.colNoEditable = list(args)
        
    def disableEdit(self, *args):
        for i in range(self.rowCount()):
            ar = list(args)
            for col in range(ar[0], ar[1]):
                item = self.item(i, col)
                if item != None:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        
    def setColumnBackground(self, columns, rgb):
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                if column in columns:
                    item = self.item(row, column)
                    if item != None:
                        item.background()
                        item.setBackground(QColor(240, 240, 240)) 
        
    def setColNoEditable(self, *args):
        colNoEditable = list(args)
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                item = self.item(row, column)
                if item is None:
                    item = QTableWidgetItem()
                    self.setItem(row, column, item)
                # Set editable or not based on the content (for demonstration purposes)
                if column in colNoEditable:
                    if item is not None:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                        
    def getData(self) -> list:
        row_count = self.rowCount()
        column_count = self.columnCount()
        table_data = []
        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                item = self.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            table_data.append(row_data)
        return table_data
    

    def getHorizontalLabels(self):
        labels = []
        for i in range(self.columnCount()):
            labels.append(self.horizontalHeaderItem(i).text())
        return labels