from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from qfluentwidgets import CheckBox
from ....components import BigDialog, TableView

class DiaconChooseDialog(BigDialog):
    def __init__(self, parent=None):
        super().__init__("Diakona", parent)
        self.table = TableView(self)
        self.dataChecked = []
        self.labels = ["ID", "Anarana", ""]
        self.table.setHorizontalHeaderLabels(self.labels)
        self.table.setRowCount(0)
        self.table.setColumnCount(len(self.labels))
        self.table.setMinimumHeight(300)
        self.contentLayout.addWidget(self.table)
        self.contentLayout.setAlignment(Qt.AlignTop)
        
    def setData(self, data:list):
        self.table.setData(data)
        for row in range(0, self.table.rowCount()):
            '''checkBoxItem = QTableWidgetItem()
            checkBoxItem.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            checkBoxItem.setCheckState(Qt.Unchecked)'''
            checkBoxItem = CheckBox()
            item = self.table.item(row, 1)
            if item.text() in self.dataChecked:
                checkBoxItem.setChecked(True)
            checkBoxItem.stateChanged.connect(lambda state, r=row : self.__changeState(state, r))
            self.table.setCellWidget(row, 2, checkBoxItem)
            
    def __changeState(self, state, row):
        data = [item[1] for item in self.table.getData()]
        selected = data[row]
        if state == 2:
            if selected not in self.dataChecked:
                self.dataChecked.append(selected)
        else:
            if selected in self.dataChecked:
                self.dataChecked.remove(selected)
        
    def allChecked(self):
        dataStr = ' - '.join([item for item in self.dataChecked])
        if dataStr.find(' - ') == 0:
            dataStr = dataStr[3:]
        return dataStr