from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import QDate
from qfluentwidgets import LineEdit, BodyLabel, ComboBox, CompactSpinBox, DateEdit


class LineEditWithLabel(QVBoxLayout):
    def __init__(self, label:str, parent=None):
        super().__init__(parent)
        self.setSpacing(2)
        self.lineEdit = LineEdit(parent)
        self.label = BodyLabel(label)
        self.addWidget(self.label)
        self.addWidget(self.lineEdit)

class DateEditWithLabel(QVBoxLayout):
    def __init__(self, label:str, parent=None):
        super().__init__(parent)
        self.setSpacing(2)
        self.lineEdit = DateEdit(parent)
        self.lineEdit.setDate(QDate(1950,1,1))
        self.label = BodyLabel(label)
        self.addWidget(self.label)
        self.addWidget(self.lineEdit)
        
    def text(self) -> str:
        value = self.lineEdit.text()
        return value if value != "01/01/1950" else ""
        
class ComboxEditWithLabel(QVBoxLayout):
    def __init__(self, label:str, data=[], parent=None):
        super().__init__(parent)
        self.setSpacing(2)
        self.combox = ComboBox(parent)
        self.combox.addItems(data)
        self.label = BodyLabel(label)
        self.addWidget(self.label)
        self.addWidget(self.combox)
        
class SpinBoxEditWithLabel(QVBoxLayout):
    def __init__(self, label:str, parent=None):
        super().__init__(parent)
        self.setSpacing(2)
        self.spinbox = CompactSpinBox(parent)
        self.label = BodyLabel(label)
        self.addWidget(self.label)
        self.addWidget(self.spinbox)
        