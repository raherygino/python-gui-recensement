from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QBoxLayout, QSizePolicy
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from qfluentwidgets import ComboBox, PrimaryPushButton, CommandBar, FluentIcon, Action, \
    ToolButton, PushButton, RoundMenu, SearchLineEdit, IndeterminateProgressBar, \
    TransparentDropDownPushButton, LineEdit, SmoothScrollArea, PixmapLabel, SubtitleLabel, StrongBodyLabel, \
        CheckBox, BodyLabel
from ...components import TableView, LineEditWithLabel, ComboxEditWithLabel
from ...common.config import OptionsConfigItem

class AddBelieverInterface(QWidget):
    
    def __init__(self,  parent=None):
        super().__init__(parent=parent)
        self.mainLayout = QVBoxLayout()
        self.scroll_area = SmoothScrollArea()
        self.scroll_area.setStyleSheet("SmoothScrollArea {border: none; background: rgba(255,255,255,0)}")
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.__contentWidgets())
        self.scroll_area.setWidgetResizable(True)
        self.mainLayout.addWidget(self.scroll_area)
        self.btnAdd = PrimaryPushButton("Ajouter", self)
        self.mainLayout.addWidget(self.btnAdd)
        self.setLayout(self.mainLayout)
        self.setObjectName("addStudentInterface")
        
    def __contentWidgets(self) -> QWidget:
        scrollable_widget = QWidget()
        scrollable_widget.setStyleSheet("QWidget {background: rgba(255,255,255,0)}")
        self.vBoxlayout = QVBoxLayout()
        self.vBoxlayout.setAlignment(Qt.AlignTop)
        self.vBoxlayout.setContentsMargins(25,10,25,10)
        self.__content()
        scrollable_widget.setLayout(self.vBoxlayout)
        return scrollable_widget
    
    def addChild(self, parent, children):
        for child in children:
            if isinstance(child, QWidget):
                parent.addWidget(child)
            else:
                parent.addLayout(child)
                
    def __content(self):
        
        self.titleLFamily = SubtitleLabel("LOHA-MPIANAKAVIA")
        self.vBoxlayout.addWidget(self.titleLFamily)
        self.vBoxlayout.setSpacing(12)
        self.row1 = QHBoxLayout()
        self.lastnameEdit = LineEditWithLabel("Anarana")
        self.firstnameEdit = LineEditWithLabel("Fanampiny")
        self.addressEdit = LineEditWithLabel("Adiresy")
        self.regionEdit = LineEditWithLabel("Faritra")
        self.addChild(self.row1, [self.lastnameEdit, self.firstnameEdit, self.addressEdit, self.regionEdit])
        
        self.row2 = QHBoxLayout()
        self.diaconEdit = LineEditWithLabel("Diakonina miandraikitra")
        self.birthdayEdit = LineEditWithLabel("Daty nahaterahana")
        self.birthplaceEdit = LineEditWithLabel("Toerana nahaterahana")
        self.addChild(self.row2, [self.diaconEdit, self.birthdayEdit, self.birthplaceEdit])
        
        self.row3 = QHBoxLayout()
        self.nameFatherEdit = LineEditWithLabel("Anaran'i Ray")
        self.nameMotherEdit = LineEditWithLabel("Anaran'i Reny")
        self.addChild(self.row3, [self.nameFatherEdit, self.nameMotherEdit])
        
        self.row4 = QHBoxLayout()
        self.baptismDateEdit = LineEditWithLabel("Daty ny batisa")
        self.baptismPlaceEdit = LineEditWithLabel("Toerana ny batisa")
        self.addChild(self.row4, [self.baptismDateEdit, self.baptismPlaceEdit])
        
        self.row5 = QHBoxLayout()
        self.recipientDateEdit = LineEditWithLabel("Daty nahampandray")
        self.recipientPlaceEdit = LineEditWithLabel("Toerana nahampandray")
        self.recipientNumberEdit = LineEditWithLabel("Laharana ny mpandray")
        self.addChild(self.row5, [self.recipientDateEdit, self.recipientPlaceEdit, self.recipientNumberEdit])
        
        self.row6 = QHBoxLayout()
        self.phoneEdit = LineEditWithLabel("Laharan'ny finday")
        self.deptWorkEdit = LineEditWithLabel("Sampana na/sy sampan'asa")
        self.responsibilityEdit = LineEditWithLabel("Andraikitra")
        self.addChild(self.row6, [self.phoneEdit, self.deptWorkEdit, self.responsibilityEdit])
        
        self.row7 = QHBoxLayout()
        
        self.titleFamily = SubtitleLabel("FIANAKAVIA")
        self.btnAddFamily = ToolButton(FluentIcon.ADD, self)
        self.familyTableView = TableView(self)
        self.row7.addWidget(self.titleFamily)
        self.row7.addWidget(self.btnAddFamily)
        self.row7.setAlignment(Qt.AlignLeft)
        #self.familyTableView.setHorizontalHeaderLabels()
        self.familyTableView.setMinimumHeight(200)
    
        self.addChild(self.vBoxlayout, [self.row1, self.row2, self.row3, 
                                        self.row4, self.row5, self.row6, 
                                        self.row7, self.familyTableView])
        
