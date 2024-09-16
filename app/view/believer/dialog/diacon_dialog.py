from PyQt5.QtWidgets import QHBoxLayout, QTableWidgetItem
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QCursor, QKeyEvent, QMouseEvent

from qfluentwidgets import Dialog, Action, RoundMenu, MenuAnimationType, FluentIcon, ToolButton, PrimaryToolButton
from ....components import SpinBoxEditWithLabel, TableView, BigDialog, LineEditWithLabel

class DiaconDialog(BigDialog):
    
    def __init__(self, parent=None):
        super().__init__('Diakona', parent)
        self.row = QHBoxLayout()
        self.btnGroup = QHBoxLayout()
        self.btnAdd = PrimaryToolButton(FluentIcon.ACCEPT)
        self.btnAdd.clicked.connect(self.__addItem)
        self.btnAdd.setEnabled(False)
        #self.btnExport= ToolButton(FluentIcon.SHARE)
        self.btnGroup.addWidget(self.btnAdd)
        #self.btnGroup.addWidget(self.btnExport)
        self.btnGroup.setAlignment(Qt.AlignBottom)
        self.nameDiacon = LineEditWithLabel("Anarana diakona")
        self.nameDiacon.lineEdit.textChanged.connect(self.__nameChanged)
        
        self.row.addLayout(self.nameDiacon)
        self.row.addLayout(self.btnGroup)
        
        self.table = TableView(self)
        self.table.contextMenuEvent = lambda event: self.contextMenu(event)
        self.table.itemClicked.connect(self.itemClicked)
        self.table.keyPressEvent = self.keyPress
        self.table.setHorizontalHeaderLabels(["ID",  "Anarana sy fanampiny"])
        self.table.setRowCount(0)
        self.table.setColumnCount(2)
        self.table.setMinimumHeight(300)
        self.contentLayout.addLayout(self.row)
        self.contentLayout.addWidget(self.table)
        self.contentLayout.setAlignment(Qt.AlignTop)
        self.table.resizeColumnsToContents()
        
    def getWidth(self):
        item = self.table.cellWidget(0,0)
        return item
        
    def keyPress(self, event: QKeyEvent | None) -> None:
        if event.key() == Qt.Key_Delete:
            items = self.table.selectionModel().selectedRows()
            if len(items) > 0:
                self.deleteSubject(items)
        
    def itemClicked(self, item: QTableWidgetItem):
        if item.column() == 0:
            for i in range(self.table.columnCount()):
                self.table.item(item.row(), i).setSelected(True)
        
    def itemRightClicked(self, item: QTableWidgetItem):
        for i in range(0, self.table.columnCount()):
            self.table.item(item.row(), i).setSelected(True)
        
    def contextMenu(self, event):
        for item in self.table.selectedItems():
            self.itemRightClicked(item)
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
        nameDiacon = self.nameDiacon.lineEdit.text()
        count = self.table.rowCount()
        self.table.setRowCount(count+1)
        self.table.setItem(count, 1, QTableWidgetItem(nameDiacon))
        self.nameDiacon.lineEdit.setText("")

    def __nameChanged(self, text):
        self.btnAdd.setEnabled(len(text) > 3)
        