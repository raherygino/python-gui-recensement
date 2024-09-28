from PyQt5.QtWidgets import QHBoxLayout, QWidget

from ....components import BigDialog, LineEditWithLabel, ComboxEditWithLabel, DateEditWithLabel, CheckBoxWithLabel

class AddFamilyDialog(BigDialog):
    
    def __init__(self, parent=None):
        super().__init__("Finakaviana", parent)
        self.row1 = QHBoxLayout()
        self.lastnameEdit = LineEditWithLabel("Anarana")
        #self.lastnameEdit.lineEdit.textChanged.connect(self.__isValidate)
        self.firstnameEdit = LineEditWithLabel("Fanampiny")
        self.addressEdit = LineEditWithLabel("Adiresy")
        self.regionEdit = ComboxEditWithLabel("Faritra", ["AVARATRA", "ATSIMO"])
        self.regionEdit.combox.currentTextChanged.connect(self.__regionChanged)
        self.addChild(self.row1, [self.lastnameEdit, self.firstnameEdit, self.addressEdit, self.regionEdit])
        
        self.row2 = QHBoxLayout()
        self.diaconEdit = ComboxEditWithLabel("Diakonina miandraikitra", ['-'])
        self.birthdayEdit = DateEditWithLabel("Daty nahaterahana")
        self.birthplaceEdit = LineEditWithLabel("Toerana nahaterahana")
        self.addChild(self.row2, [self.diaconEdit, self.birthdayEdit, self.birthplaceEdit])
        
        self.row3 = QHBoxLayout()
        self.nameFatherEdit = LineEditWithLabel("Anaran'i Ray")
        self.nameMotherEdit = LineEditWithLabel("Anaran'i Reny")
        self.addChild(self.row3, [self.nameFatherEdit, self.nameMotherEdit])
        
        self.row4 = QHBoxLayout()
        self.baptismDateEdit = DateEditWithLabel("Daty ny batisa")
        self.baptismPlaceEdit = LineEditWithLabel("Toerana ny batisa")
        self.addChild(self.row4, [self.baptismDateEdit, self.baptismPlaceEdit])
        
        self.row5 = QHBoxLayout()
        self.recipientDateEdit = DateEditWithLabel("Daty nahampandray")
        self.recipientPlaceEdit = LineEditWithLabel("Toerana nahampandray")
        self.recipientNumberEdit = LineEditWithLabel("Laharana ny mpandray")
        self.recipientNumberEdit.lineEdit.setText("A ")
        self.addChild(self.row5, [self.recipientDateEdit, self.recipientPlaceEdit, self.recipientNumberEdit])
        
        self.row6 = QHBoxLayout()
        self.phoneEdit = LineEditWithLabel("Laharan'ny finday")
        self.responsibilityEdit = LineEditWithLabel("Andraikitra")
        self.workEdit = LineEditWithLabel("Asa")
        self.addChild(self.row6, [self.phoneEdit,  self.responsibilityEdit, self.workEdit])
        
        self.row7 = QHBoxLayout()
        self.deptWorkCheck = CheckBoxWithLabel("Sampana na/sy sampan'asa")
    
        self.addChild(self.contentLayout, [self.row1, self.row2, self.row3, 
                                        self.row4, self.row5, self.row6,  self.deptWorkCheck])
        self.resize(800, 600)
        
    def __regionChanged(self, text):
        self.recipientNumberEdit.lineEdit.setText("A " if text == "ATSIMO" else "B ")
        
    def addChild(self, parent, children):
        for child in children:
            if isinstance(child, QWidget):
                parent.addWidget(child)
            else:
                parent.addLayout(child)