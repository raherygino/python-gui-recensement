from PyQt5.QtWidgets import QHBoxLayout, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QCursor

from qfluentwidgets import Dialog, Action, RoundMenu, MenuAnimationType, FluentIcon, PrimaryToolButton, ToolButton
from ....components import TableView, BigDialog, LineEditWithLabel, ConfirmDialog, ImportDialog, PrimaryButton, Button

class ToolDialog(BigDialog):
    
    def __init__(self, title:str, labels:list[str], parent=None):
        super().__init__(title, parent)
        self.row = QHBoxLayout()
        self.btnGroup = QHBoxLayout()
        self.btnAdd = PrimaryToolButton(FluentIcon.ACCEPT)
        self.btnImport = ToolButton(FluentIcon.DOWNLOAD)
        self.btnImport.clicked.connect(lambda: self.importData())
        self.btnAdd.clicked.connect(self.__addItem)
        self.btnAdd.setEnabled(False)
        self.btnGroup.addWidget(self.btnAdd)
        self.btnGroup.addWidget(self.btnImport)
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
        self.yesBtn.setText("Ekena")
        self.cancelBtn.setText("Asorina")
        
    def setData(self, data:list):
        self.data = self.table.getData()
        ps = len(self.data)
        self.table.setRowCount(ps+len(data))
        for row, item in enumerate(data):
            for column, nItem in enumerate(item):
                widgetItem = QTableWidgetItem(str(nItem))
                if column == 0:
                    widgetItem.setFlags(widgetItem.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(ps+row, column, widgetItem)
        self.table.resizeColumnsToContents()
      
    def contextMenu(self, event):
        items = self.table.selectionModel().selectedRows()
        if len(items) > 0:
            menu = RoundMenu(parent=self)
            menu.addAction(Action(FluentIcon.DELETE, 'Fafana', triggered = lambda:self.deleteSubject(items)))
            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
        
    def deleteSubject(self, items):
        dialog = ConfirmDialog('Fafana', 'Hofafana marina ve?',self)
        dialog.yesBtn.setText("Eny")
        dialog.cancelBtn.setText("Tsia")
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
        self.btnAdd.setEnabled(len(text) > 2)
        
    def exportData(self):
        data = self.table.getData()
        if len(data) > 0:
            destination_path, _ = QFileDialog.getSaveFileName(self, "Exporter", "", "All Files (*);;Text Files (*.csv)")
            if destination_path:
                with open(destination_path, 'w') as f:
                    for item in data:
                        line = ";".join([nItem for nItem in item])
                        f.writelines(f'{line}\n')
        else:
            self.utils.infoBarError('Erreur', "Aucune donnée à exporter", self)
        
    def importData(self):
        destination_path, _ = QFileDialog.getOpenFileName(self, "Importer", "", "CSV File (*.csv)")
        if destination_path:
            lenData = len(self.table.getData())
            with open(destination_path, 'r') as f:
                data = []
                for i, line in enumerate(f):
                    i = lenData + i
                    nLine = line.replace("\n", "").split(";")
                    nLine.insert(0, '')
                    data.append(nLine)
                self.setData(data)
                '''dialogImport = ImportDialog(data, self.table.getHorizontalLabels(), self)
                dialogImport.yesBtn.clicked.connect(lambda:  self.addToTable(dialogImport))
                dialogImport.exec()'''
                
    def addToTable(self, dialogImport: ImportDialog):
        nData = dialogImport.getData()
        first =  []
        '''for nItem in nData[0]:
            if nItem != None:
                first.append(nItem)
        if len(first) == 0:
            print('Aucune données n\'a été choisi!')
            #self.utils.infoBarError('Erreur', 'Aucune données n\'a été choisi!', dialog)
        else:
            for i, item in enumerate(nData):
                self.table.insertRow(i)
                for j, nItem in enumerate(item):
                    qWidget = QTableWidgetItem(nItem)
                    self.table.setItem(i, j, qWidget)
            dialogImport.accept()'''
        