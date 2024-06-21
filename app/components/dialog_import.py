from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, ComboBox, BodyLabel

class DialogImport(MessageBoxBase):
    def __init__(self, firstData:list, columns:list, parent=None):
        super().__init__(parent)
        self.viewLayout.addWidget(SubtitleLabel('Importer', self))
        self.setMinimumWidth(350)
        row = QHBoxLayout()
        titleVal = BodyLabel("Valeur")
        titleCol = BodyLabel("Colonne")
        row.addWidget(titleVal)
        row.addWidget(titleCol, 0, Qt.AlignRight)
        self.viewLayout.addLayout(row)
        columns.insert(0, "-")
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
            self.viewLayout.addLayout(row)