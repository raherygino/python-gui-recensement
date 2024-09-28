from PyQt5.QtWidgets import QHBoxLayout, QWidget

from ....components import BigDialog, LineEditWithLabel, ComboxEditWithLabel, DateEditWithLabel, CheckBoxWithLabel
from ....models import Believer
from ....common import Function

class AddFamilyDialog(BigDialog):
    
    def __init__(self, parent=None):
        super().__init__("Finakaviana", parent)
        self.func = Function()
        self.row1 = QHBoxLayout()
        self.row1.setSpacing(12)
        self.lastnameEdit = LineEditWithLabel("Anarana")
        self.lastnameEdit.lineEdit.textChanged.connect(self.__isValid)
        self.firstnameEdit = LineEditWithLabel("Fanampiny")
        self.posFamilyCombox = ComboxEditWithLabel("Amin'ny finakaviana", ["Zanaka", "Vady"])
        self.posFamilyCombox.combox.currentTextChanged.connect(self.__posFamilyChanged)
        self.genderCombox = ComboxEditWithLabel("Lahy / Vavy", ["Lahy", "Vavy"])
        self.addChild(self.row1, [self.lastnameEdit, self.firstnameEdit, self.posFamilyCombox, self.genderCombox])
        
        self.row2 = QHBoxLayout()
        self.addressEdit = LineEditWithLabel("Adiresy")
        self.regionEdit = ComboxEditWithLabel("Faritra", ["AVARATRA", "ATSIMO"])
        self.regionEdit.combox.currentTextChanged.connect(self.__regionChanged)
        self.addChild(self.row2, [self.addressEdit, self.regionEdit])
        
        self.row3 = QHBoxLayout()
        self.diaconEdit = ComboxEditWithLabel("Diakonina miandraikitra", ['-'])
        self.birthdayEdit = DateEditWithLabel("Daty nahaterahana")
        self.birthplaceEdit = LineEditWithLabel("Toerana nahaterahana")
        self.addChild(self.row3, [self.diaconEdit, self.birthdayEdit, self.birthplaceEdit])
        
        
        self.row4 = QHBoxLayout()
        self.baptismDateEdit = DateEditWithLabel("Daty ny batisa")
        self.baptismPlaceEdit = LineEditWithLabel("Toerana ny batisa")
        self.addChild(self.row4, [self.baptismDateEdit, self.baptismPlaceEdit])
        
        self.row5 = QHBoxLayout()
        self.recipientDateEdit = DateEditWithLabel("Daty nahampandray")
        self.recipientPlaceEdit = LineEditWithLabel("Toerana nahampandray")
        self.recipientNumberEdit = LineEditWithLabel("Laharana ny mpandray")
        self.recipientNumberEdit.lineEdit.setText("B ")
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
        
        self.yesBtn.setText("Ampidirin")
        self.cancelBtn.setText("Esorina")
        self.__isValid(self.lastnameEdit.lineEdit.text())
        
    def data(self):
        dRec =  self.recipientDateEdit.lineEdit.text()
        return Believer(
            lastname=self.lastnameEdit.lineEdit.text(),
            firstname = self.firstnameEdit.lineEdit.text(),
            gender = self.genderCombox.combox.currentText(),
            pos_family = self.posFamilyCombox.combox.currentText(),
            address = self.addressEdit.lineEdit.text(),
            region = self.regionEdit.combox.currentText(),
            diacon = self.diaconEdit.combox.currentText(),
            birthday = self.birthdayEdit.lineEdit.text(),
            birthplace = self.birthplaceEdit.lineEdit.text(),
            name_father = "",
            id_father = 0,
            name_mother = "",
            id_mother = 0,
            date_of_baptism = self.baptismDateEdit.lineEdit.text(),
            place_of_baptism = self.baptismPlaceEdit.lineEdit.text(),
            date_of_recipient = "" if dRec == "01/01/1950" else dRec,
            place_of_recipient = self.recipientPlaceEdit.lineEdit.text(),
            number_recipient = self.recipientNumberEdit.lineEdit.text(),
            phone = self.phoneEdit.lineEdit.text(),
            dept_work = self.deptWorkCheck.itemsCheckedText(),
            responsibility = self.responsibilityEdit.lineEdit.text(),
            work = self.workEdit.lineEdit.text()
        )
        
    def setData(self, data:Believer):
        self.lastnameEdit.lineEdit.setText(data.lastname)
        self.firstnameEdit.lineEdit.setText(data.firstname)
        self.genderCombox.combox.setCurrentText(data.gender)
        self.posFamilyCombox.combox.setCurrentText(data.pos_family)
        self.addressEdit.lineEdit.setText(data.address)
        self.regionEdit.combox.setCurrentText(data.region)
        self.diaconEdit.combox.setCurrentText(data.diacon)
        self.birthdayEdit.lineEdit.setDate(self.func.strToQDate(data.birthday))
        self.birthplaceEdit.lineEdit.setText(data.birthplace)
        self.baptismDateEdit.lineEdit.setDate(self.func.strToQDate(data.date_of_baptism))
        self.baptismPlaceEdit.lineEdit.setText(data.place_of_baptism)
        self.recipientDateEdit.lineEdit.setDate(self.func.strToQDate(data.date_of_recipient))
        self.recipientPlaceEdit.lineEdit.setText(data.place_of_recipient)
        self.recipientNumberEdit.lineEdit.setText(data.place_of_recipient)
        self.phoneEdit.lineEdit.setText(data.phone)
        self.deptWorkCheck.check(data.dept_work)
        self.responsibilityEdit.lineEdit.setText(data.responsibility)
        self.workEdit.lineEdit.setText(data.work)
        self.yesBtn.setText("Ovaina")
        
    def __isValid(self, text):
        self.yesBtn.setEnabled(len(text) > 3)
        
    def __posFamilyChanged(self, text):
        isWife = text == "Vady"
        if isWife:
            self.genderCombox.combox.setCurrentIndex(1)
        self.genderCombox.combox.setDisabled(isWife)
        
    def __regionChanged(self, text):
        self.recipientNumberEdit.lineEdit.setText("A " if text == "ATSIMO" else "B ")
        
    def addChild(self, parent, children):
        for child in children:
            if isinstance(child, QWidget):
                parent.addWidget(child)
            else:
                parent.addLayout(child)