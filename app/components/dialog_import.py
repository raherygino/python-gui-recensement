from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import Dialog, SubtitleLabel, LineEdit, ComboBox, BodyLabel, PrimaryPushButton,\
    PushButton

class DialogImport(Dialog):
    def __init__(self, data:list, columns:list, parent=None):
        super().__init__('', '', parent)
        self.setTitleBarVisible(False)
        self.titleLabel.setVisible(False)
        self.contentLabel.setVisible(False)
        columns.insert(0, "-")
        self.textLayout.addWidget(SubtitleLabel('Importer', self))
        self.setFixedWidth(400)
        self.data =  data
        row = QHBoxLayout()
        row.addWidget(BodyLabel("Valeur"))
        row.addWidget(BodyLabel("Colonne"), 0, Qt.AlignRight)
        self.textLayout.addLayout(row)
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
            self.textLayout.addLayout(row)
        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.yesBtn = PrimaryPushButton("Ok")
        self.cancelBtn = PushButton('Annuler')
        self.cancelBtn.clicked.connect(self.reject)
        self.buttonLayout.addWidget(self.yesBtn)
        self.buttonLayout.addWidget(self.cancelBtn)
        
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