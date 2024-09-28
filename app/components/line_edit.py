from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import QDate, QEasingCurve, QParallelAnimationGroup
from qfluentwidgets import LineEdit, BodyLabel, ComboBox, CompactSpinBox, DateEdit, FlowLayout, CheckBox


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

class CheckBoxWithLabel(QVBoxLayout):
    def __init__(self, label:str, parent=None):
        super().__init__(parent)
        self.nParent = parent
        self.setSpacing(2)
        self.itemsChecked = []
        self.fLayout = FlowLayout(parent, needAni=False)

        self.lineEdit = LineEdit(parent)
        self.label = BodyLabel(label)
        self.addWidget(self.label)
        self.addLayout(self.fLayout)
        
    def addData(self, data):
        # Loop over all widgets and remove them from the layout
        while self.fLayout.count():
            item = self.fLayout.takeAt(0)  # Take the item at the 0 index
            item.deleteLater()
        for item in data:
            checkbox = CheckBox(item, self.nParent)
            checkbox.stateChanged.connect(self.__checkboxChanged)
            self.fLayout.addWidget(checkbox)
    
    def __checkboxChanged(self):
        sender = self.sender()
        if sender.isChecked():
            self.itemsChecked.append(sender.text())
        else:
            self.itemsChecked.remove(sender.text())
        
    def getItemChecked(self):
        return self.itemsChecked
    
    def itemsCheckedText(self):
        text = ""
        for item in self.itemsChecked:
            text += f'{item}, '
        return text[0:len(text)-2]
        
        