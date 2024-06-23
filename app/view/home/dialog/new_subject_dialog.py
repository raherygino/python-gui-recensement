from PyQt5.QtWidgets import QHBoxLayout, QTableWidgetItem
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QCursor, QKeyEvent

from qfluentwidgets import Dialog, Action, RoundMenu, MenuAnimationType, \
     PrimaryPushButton, PushButton, FluentIcon, SubtitleLabel, ToolButton
from ....components.table_view import TableView
from ....components import SpinBoxEditWithLabel

class NewSubjectDialog(Dialog):

    def __init__(self, parent=None):
        super().__init__("", "", parent)
        self.setTitleBarVisible(False)
        self.titleLabel.setVisible(False)
        self.contentLabel.setVisible(False)
        self.row = QHBoxLayout()
        self.btnGroup = QHBoxLayout()
        self.title = SubtitleLabel("Matières")
        self.btnImport = ToolButton(FluentIcon.DOWNLOAD)
        self.btnExport= ToolButton(FluentIcon.SHARE)
        self.row.addWidget(self.title, 0, Qt.AlignLeft)
        self.btnGroup.addWidget(self.btnImport)
        self.btnGroup.addWidget(self.btnExport)
        self.btnGroup.setAlignment(Qt.AlignRight)
        self.row.addLayout(self.btnGroup)
        self.count = SpinBoxEditWithLabel("Nombre de matières")
        self.count.spinbox.setValue(1)
        self.count.spinbox.textChanged.connect(self.__countChange)
        self.table = TableView(self)
        self.table.contextMenuEvent = lambda event: self.contextMenu(event)
        self.table.itemClicked.connect(self.itemClicked)
        self.table.keyPressEvent = self.keyPress
        self.table.setHorizontalHeaderLabels(["ID",  "Abréviation", "Rubrique", "Coeff"])
        self.table.setRowCount(1)
        self.table.setColumnCount(4)
        self.table.setMinimumHeight(300)
        self.table.itemChanged.connect(lambda item: self.table.validateInput(3, item, "1"))
        
        self.yesBtn = PrimaryPushButton("Ok")
        self.cancelBtn = PushButton("Annuler")
        self.cancelBtn.clicked.connect(self.yesBtnClicked)
        self.textLayout.addLayout(self.row)
        self.textLayout.addLayout(self.count)
        self.textLayout.addWidget(self.table)
        
        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        
        self.buttonLayout.addWidget(self.yesBtn)
        self.buttonLayout.addWidget(self.cancelBtn)
        
        self.setFixedWidth(450)

    def keyPress(self, event: QKeyEvent | None) -> None:
        if event.key() == Qt.Key_Delete:
            items = self.table.selectionModel().selectedRows()
            if len(items) > 0:
                self.deleteSubject(items)
        
    def itemClicked(self, item: QTableWidgetItem):
        if item.column() == 0:
            for i in range(self.table.columnCount()):
                self.table.item(item.row(), i).setSelected(True)
        
    def itemRightClicked(self, item: QTableWidgetItem):
        for i in range(0, self.table.columnCount()):
            self.table.item(item.row(), i).setSelected(True)
        
    def contextMenu(self, event):
        for item in self.table.selectedItems():
            self.itemRightClicked(item)
        items = self.table.selectionModel().selectedRows()
        if len(items) > 0:
            menu = RoundMenu(parent=self)
            menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda:self.deleteSubject(items)))
            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
        
    def deleteSubject(self, items):
        dialog = Dialog("Supprimer?", "Voulez vous supprimer vraiment?", self)
        dialog.setTitleBarVisible(False)
        if dialog.exec():
            for index in sorted(items, key=lambda x: x.row(), reverse=True):
                self.table.removeRow(index.row())

    def __countChange(self, value):
        self.table.setRowCount(int(value))
        self.table.setColNoEditable(0)

    def yesBtnClicked(self):
        self.close()

        