from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from qfluentwidgets import StrongBodyLabel, PrimaryToolButton, ToolButton, FluentIcon, CheckBox, SmoothScrollArea

from .teaching_tip import FlyoutViewBase

class FilterFlyoutView(FlyoutViewBase):

    def __init__(self,title:str, items, itemsChecked:list, parent=None):
        super().__init__(parent)
        self.nParent = parent
        self.mLayout = QVBoxLayout(self)
        self.title = title
        self.label = StrongBodyLabel(title)
        self.label.setAlignment(Qt.AlignCenter)
        self.data = items
        self.itemsChecked = itemsChecked
        
        self.yesButton = PrimaryToolButton(FluentIcon.ACCEPT)
        self.noButton = ToolButton(FluentIcon.CLOSE)
        
        self.mLayout.setSpacing(12)
        self.mLayout.setContentsMargins(12, 12, 12, 12)
        self.mLayout.addWidget(self.label)
        
        self.scroll_area = SmoothScrollArea()
        self.scroll_area.setStyleSheet("SmoothScrollArea {border: none; background: rgba(255,255,255,0)}")
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.wgt = self.__contentWidgets()
        self.scroll_area.setWidget(self.wgt)
        self.scroll_area.setWidgetResizable(True)
        self.mLayout.addWidget(self.scroll_area)
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setContentsMargins(0,0,0,0)
        self.hBoxLayout.setSpacing(6)
        self.hBoxLayout.setAlignment(Qt.AlignRight)
        self.hBoxLayout.addWidget(self.yesButton)
        self.hBoxLayout.addWidget(self.noButton)
        self.mLayout.addLayout(self.hBoxLayout)
    
    def __contentWidgets(self) -> QWidget:
        scrollable_widget = QWidget()
        scrollable_widget.setStyleSheet("QWidget {background: rgba(255,255,255,0)}")
        self.vBoxlayout = QVBoxLayout()
        self.vBoxlayout.setAlignment(Qt.AlignTop)
        self.addItems(self.data)
        scrollable_widget.setLayout(self.vBoxlayout)
        return scrollable_widget
        
    def addItems(self, items):
        itemsChecked = [f'{item}{'ère' if item == '1' else 'ème'} {self.title}' if item.find('è') == -1 else item for item in self.itemsChecked] if self.title == "Compagnie" or self.title == "Section" else self.itemsChecked
        self.checkboxAll = CheckBox("Tous")
        self.checkboxAll.setChecked(len(self.data)-len(itemsChecked) == 0)
        self.checkboxAll.stateChanged.connect(self.setCheckAll)
        self.vBoxlayout.addWidget(self.checkboxAll)
        for item in items:
            checkbox = CheckBox(item)
            if item in itemsChecked:
                checkbox.setChecked(True)
            self.vBoxlayout.addWidget(checkbox)
    
    def setCheckAll(self, val):
        children = self.wgt.children()
        intPos = children.index(self.findChild(CheckBox)) + 1
        for i, item in enumerate(self.data):
            checkBox: CheckBox = children[intPos+i]
            checkBox.setChecked(val == 2)
            
    def getDataFilter(self, popup):
        popup.close()
        children = self.wgt.children()
        intPos = children.index(self.findChild(CheckBox)) + 1
        vals = []
        for i, item in enumerate(self.data):
            checkBox: CheckBox = children[intPos+i]
            if checkBox.isChecked():
                vals.append(item)
        return vals