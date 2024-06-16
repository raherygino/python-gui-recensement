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
        #self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.header = self.horizontalHeader()
        self.verticalHeader().hide()
        #self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setContentsMargins(0,0,0,0)
        self.setQss(cfg.get(cfg.theme))
        self.colNoEditable = []
        self.isIncrement = False
        
    def setHorizontalHeaderLabels(self, labels: Iterable[str | None]) -> None:
        self.setColumnCount(len(labels))
        #self.header.setSectionResizeMode(len(labels) - 1, QHeaderView.Stretch)
        return super().setHorizontalHeaderLabels(labels)
    
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
        with open(f'app/resource/{theme}.qss', encoding='utf-8') as f:
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
        '''item = self.item(1, 1)
        if item != None:
            item.setBackground(QColor(240, 240, 240))'''
        
    def setColumnNoEditable(self, *args):
        self.colNoEditable = list(args)
        
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
                        #item.setFlags(item.flags() | Qt.ItemIsEditable)
                        
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