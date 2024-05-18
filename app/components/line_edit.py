from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from qfluentwidgets import BodyLabel, LineEdit, ComboBox, CompactSpinBox, DateEdit

class editWithLabel(QVBoxLayout):
    def __init__(self, label:str,parent=None, **kwargs):
        super().__init__(None)
        self.parent = parent
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(5)
        self.label = BodyLabel(parent)
        self.label.setText(label)
        self.addWidget(self.label)
        self.args = kwargs
        self.lineEdits = []
        self.LineEdit()

    def LineEdit(self):
        self.hBoxLayout = QHBoxLayout()
        self.lineEdits.clear()
        if "placeholders" in self.args.keys():
            placeholders = self.args.get("placeholders")
            for placeholder in placeholders:
                lineEdit = LineEdit(self.parent)
                lineEdit.setClearButtonEnabled(True)
                lineEdit.setPlaceholderText(placeholder)
                self.hBoxLayout.addWidget(lineEdit)
                self.lineEdits.append(lineEdit)
                
        if "combox" in self.args.keys():
            self.combox = ComboBox(self.parent)
            self.combox.setMinimumWidth(200)
            self.combox.addItems(self.args.get("combox"))
            self.hBoxLayout.addWidget(self.combox)
            
        if "spinbox" in self.args.keys():
            self.compactSpinBox = CompactSpinBox(self.parent)
            self.hBoxLayout.addWidget(self.compactSpinBox)
            
        if "date" in self.args.keys():
            self.date = DateEdit(self.parent)
            self.hBoxLayout.addWidget(self.date)
            
        self.addLayout(self.hBoxLayout)
        
    
    def getValue(self) -> int:
        return self.compactSpinBox.value()
            
    def value(self):
        return self.combox.text()
    
    def text(self, pos:int):
        return self.lineEdits[pos].text()
    
    def lineEdit(self, pos:int) -> LineEdit:
        return self.lineEdits[pos]
        