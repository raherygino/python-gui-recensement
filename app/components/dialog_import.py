from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, ComboBox, BodyLabel

class DialogImport(MessageBoxBase):
    def __init__(self, data:list, columns:list, parent=None):
        super().__init__(parent)
        self.viewLayout.addWidget(SubtitleLabel('Importer', self))
        self.setMinimumWidth(350)
        self.data =  data
        row = QHBoxLayout()
        row.addWidget(BodyLabel("Valeur"))
        row.addWidget(BodyLabel("Colonne"), 0, Qt.AlignRight)
        self.viewLayout.addLayout(row)
        columns.insert(0, "-")
        self.items = []
        firstData = data[0]
        for i, item in enumerate(firstData):
            row = QHBoxLayout()
            lineEdit = LineEdit(self)
            lineEdit.setText(item)
            lineEdit.setReadOnly(True)
            comboBox =  ComboBox(self)
            comboBox.addItems(columns)
            comboBox.setCurrentIndex(i+1 if i+1 < len(columns) else 0)
            row.addWidget(lineEdit)
            row.addWidget(comboBox)
            self.items.append(comboBox)
            self.viewLayout.addLayout(row)
            
    def getData(self):
        data = [item.currentIndex()-1 for item in self.items]
        nData = []
        for nItem in self.data:
            newItem = [None] * len(data)
            for i, n in enumerate(data):
                if n != -1:
                    newItem[n] = nItem[i]
            nData.append(newItem)
        return nData