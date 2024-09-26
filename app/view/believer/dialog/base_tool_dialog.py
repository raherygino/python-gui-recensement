from PyQt5.QtWidgets import QHBoxLayout, QTableWidgetItem
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QCursor

from qfluentwidgets import Dialog, Action, RoundMenu, MenuAnimationType, FluentIcon, PrimaryToolButton
from ....components import TableView, BigDialog, LineEditWithLabel

class ToolDialog(BigDialog):
    
    def __init__(self, title:str, labels:list[str], parent=None):
        super().__init__(title, parent)
        self.row = QHBoxLayout()
        self.btnGroup = QHBoxLayout()
        self.btnAdd = PrimaryToolButton(FluentIcon.ACCEPT)
        self.btnAdd.clicked.connect(self.__addItem)
        self.btnAdd.setEnabled(False)
        self.btnGroup.addWidget(self.btnAdd)
        self.btnGroup.setAlignment(Qt.AlignBottom)
        for label in labels:
            editLine = LineEditWithLabel(label)
            self.row.addLayout(editLine)
        self.row.children()[0].lineEdit.textChanged.connect(self.__nameChanged)
        self.row.addLayout(self.btnGroup)
        self.table = TableView(self)
        self.table.contextMenuEvent = lambda event: self.contextMenu(event)
        self.labels = ["ID"]
        self.labels.extend([label for label in labels])
        self.table.setHorizontalHeaderLabels(self.labels)
        self.table.setRowCount(0)
        self.table.setColumnCount(len(self.labels))
        self.table.setMinimumHeight(300)
        self.contentLayout.addLayout(self.row)
        self.contentLayout.addWidget(self.table)
        self.contentLayout.setAlignment(Qt.AlignTop)
        self.table.resizeColumnsToContents()
        
        
    def setData(self, data:list):
        self.table.setRowCount(len(data))
        for row, item in enumerate(data):
            for column, nItem in enumerate(item):
                widgetItem = QTableWidgetItem(str(nItem))
                if column == 0:
                    widgetItem.setFlags(widgetItem.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, column, widgetItem)
        self.table.resizeColumnsToContents()
      
    def contextMenu(self, event):
        items = self.table.selectionModel().selectedRows()
        if len(items) > 0:
            menu = RoundMenu(parent=self)
            menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda:self.deleteSubject(items)))
            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
        
    def deleteSubject(self, items):
        dialog = Dialog("Supprimer?", "Voulez vous supprimer vraiment?", self)
        dialog.setTitleBarVisible(False)
        if dialog.exec():
            for index in sorted(items, key=lambda x: x.row(), reverse=True):
                self.table.removeRow(index.row())
                
    def __addItem(self):
        count = self.table.rowCount()
        self.table.setRowCount(count+1)
        data = []
        for child in self.row.children():
            if type(child).__name__ == "LineEditWithLabel":
                data.append(child.lineEdit.text())
                child.lineEdit.setText("")
        for i, item in enumerate(data):
            self.table.setItem(count, i+1, QTableWidgetItem(item))
        self.table.resizeColumnsToContents()

    def __nameChanged(self, text):
        self.btnAdd.setEnabled(len(text) > 3)
        