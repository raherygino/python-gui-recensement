from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QCursor

from qfluentwidgets import Dialog, Action, RoundMenu, MenuAnimationType, \
     PrimaryPushButton, PushButton, FluentIcon
from ....components.table_view import TableView
from ....components import SpinBoxEditWithLabel

class NewSubjectDialog(Dialog):

    def __init__(self, parent=None):
        super().__init__("Matières", "", parent)
        self.setTitleBarVisible(False)
        self.contentLabel.setVisible(False)
        
        self.row = QHBoxLayout()
        self.count = SpinBoxEditWithLabel("Nombre de matières")
        self.count.spinbox.setValue(1)
        self.count.spinbox.textChanged.connect(self.__countChange)
        
        self.table = TableView(self)
        self.table.contextMenuEvent = lambda event: self.contextMenu(event)
        self.table.setHorizontalHeaderLabels(["ID",  "Abréviation", "Rubrique", "Coeff"])
        self.table.setRowCount(1)
        self.table.setColumnCount(4)
        self.table.setMinimumHeight(300)
        self.table.itemChanged.connect(lambda item: self.table.validateInput(3, item, "1"))
        
        self.yesBtn = PrimaryPushButton("Ok")
        self.cancelBtn = PushButton("Annuler")
        self.cancelBtn.clicked.connect(self.yesBtnClicked)
        
        self.textLayout.addLayout(self.count)
        self.textLayout.addWidget(self.table)
        
        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        
        self.buttonLayout.addWidget(self.yesBtn)
        self.buttonLayout.addWidget(self.cancelBtn)
        
        self.setFixedWidth(450)
        
    def contextMenu(self, event):
        item = self.table.selectedItems()[0]
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda:self.deleteSubject(item.row())))
        self.posCur = QCursor().pos()
        cur_x = self.posCur.x()
        cur_y = self.posCur.y()
        menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
        
    def deleteSubject(self, row):
        dialog = Dialog("Supprimer?", "Voulez vous supprimer vraiment?", self)
        dialog.setTitleBarVisible(False)
        if dialog.exec():
            self.table.removeRow(row)

    def __countChange(self, value):
        self.table.setRowCount(int(value))
        self.table.setColNoEditable(0)

    def yesBtnClicked(self):
        self.close()

        