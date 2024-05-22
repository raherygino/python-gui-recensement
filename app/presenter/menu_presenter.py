from PyQt5.QtCore import QDate, QPoint
from PyQt5.QtGui import QCursor
from ..models import Believer, BelieverModel
from ..view import ShowBelieverDialog, AddBelieverInterface
from qfluentwidgets import MessageDialog, RoundMenu, Action, MenuAnimationType, FluentIcon

class MenuAction:
    
    def __init__(self, presenter) -> None:
        self.presenter = presenter
        self.view = presenter.view
        self.model: BelieverModel= self.presenter.model
        
    def show(self, itemId):
        believer: Believer = self.model.fetch_item_by_id(itemId)
        row1 = [
            ["Anarana", believer.lastname],
            ["Fanampiny", believer.firstname],
            ["Adiresy", believer.address],
            ["Faritra", believer.region],
            ["Diakonina miandraikitra", believer.diacon]
            ]
        
        row2 = [
            ["Daty sy toerana nahaterahana", f'{believer.birthday} {believer.birthplace}'],
            ["Anaran'i Reny", believer.name_mother],
            ["Anaran'i Ray", believer.name_father],
            ["Anaran'i Reny", believer.name_mother],
            ["Daty ny batisa", believer.date_of_baptism],
            ]
        
        row3 = [
            ["Toerana ny batisa", believer.place_of_baptism],
            ["Daty nahampandray", believer.date_of_recipient],
            ["Toerana nahampandray", believer.place_of_recipient],
            ["Laharana ny mpandray", believer.number_recipient],
            ["Laharan'ny finday", believer.phone],
            ]
        
        row4 = [
            ["Sampana na/sy sampan'asa", believer.dept_work],
                ["Andraikitra", believer.responsibility],
            ]
            
        allRows =  [row1, row2, row3, row4]
        dialog = ShowBelieverDialog(self.view)
        dialog.table.setHorizontalHeaderLabels(self.presenter.labelsFamily)
            
        for i, row in enumerate(allRows):
            for j, column in enumerate(row):
                dialog.addLabelValue(column[0], column[1], i,j)
                    
        data = self.model.fetch_all(id_conjoint=itemId)
        for value in self.model.fetch_all(id_father=itemId):
            data.append(value)
                
        self.presenter.setData(dialog.table, data)
        dialog.table.contextMenuEvent = lambda e, dialog = dialog, data=data: self.rightClickTable(e, data, dialog)
        dialog.exec()
        
    def rightClickTable(self, event, data, dialog):
        selectedItems = dialog.table.selectedItems()
        if len(selectedItems) != 0:
            if selectedItems[3].text() == "Lahy":
                blv = data[int(selectedItems[0].text())]
                menu = RoundMenu(parent=self.view)
                menu.addAction(
                    Action(
                        FluentIcon.PEOPLE, 
                        'Loham-pianakaviana hafa', 
                        triggered= lambda: self.newLeaderFamily(blv, dialog)))
            
                self.posCur = QCursor().pos()
                cur_x = self.posCur.x()
                cur_y = self.posCur.y()
                menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
                
    def newLeaderFamily(self, item, dialog):
        self.update(item.id)
        self.presenter.isNewLead = True
        dialog.accept()
        
    def strToQDate(self, strDate: str):
        date = strDate.split("/")
        dateOut = QDate(2000,1,1)
        if len(date) == 3:
            dateOut = QDate(int(date[2]), int(date[1]), int(date[0]))
        return dateOut
        
    def update(self, item):
        self.presenter.addView.nParent.stackedWidget.setCurrentWidget(self.presenter.addView)
        self.presenter.idEdit = int(item)
        self.presenter.isNewLead = False
        believer : Believer = self.model.fetch_item_by_id(item)
        view : AddBelieverInterface = self.presenter.addView
        view.lastnameEdit.lineEdit.setText(believer.lastname)
        view.firstnameEdit.lineEdit.setText(believer.firstname)
        view.addressEdit.lineEdit.setText(believer.address)
        view.regionEdit.lineEdit.setText(believer.region)
        view.diaconEdit.lineEdit.setText(believer.diacon)
        view.birthdayEdit.lineEdit.setDate(self.strToQDate(believer.birthday))
        view.birthplaceEdit.lineEdit.setText(believer.birthplace)
        view.nameFatherEdit.lineEdit.setText(believer.name_father)
        view.nameMotherEdit.lineEdit.setText(believer.name_mother)
        view.baptismDateEdit.lineEdit.setDate(self.strToQDate(believer.date_of_baptism))
        view.baptismPlaceEdit.lineEdit.setText(believer.place_of_baptism)
        view.recipientDateEdit.lineEdit.setDate(self.strToQDate(believer.date_of_recipient))
        view.recipientPlaceEdit.lineEdit.setText(believer.place_of_recipient)
        view.recipientNumberEdit.lineEdit.setText(believer.number_recipient)
        view.phoneEdit.lineEdit.setText(believer.phone)
        view.deptWorkEdit.lineEdit.setText(believer.dept_work)
        view.responsibilityEdit.lineEdit.setText(believer.responsibility)
        
        data = self.model.fetch_all(id_conjoint=item)
        for value in self.model.fetch_all(id_father=item):
            data.append(value)
        self.presenter.family = data
        self.presenter.setData(view.familyTableView, self.presenter.family)
        
    def confirmDelete(self, item):
        dialog = MessageDialog('Supprimer', 'Voulez vous le supprimer vraiment?', self.view.nParent)
        dialog.yesButton.clicked.connect(lambda: self.delete(item))
        dialog.exec_()
        
    def delete(self, item):
        self.model.delete_item(item)
        self.presenter.fetchData(self.model.fetch_all(**self.presenter.query))
        #self.presenter.refresh.emit()