from PyQt5.QtCore import QThread, QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFileDialog
from qfluentwidgets import FluentIcon, RoundMenu, MenuAnimationType, Action, Dialog
from ..common import Function
from ..models import DatabaseWorker, BelieverModel, Believer
from ..view import ListBelieverInterface, AddBelieverDialog, AddBelieverInterface, ShowBelieverDialog
from .menu_presenter import MenuAction
import dataclasses
import os

class BelieverPresenter:
    
    def __init__(self, model: BelieverModel, addView: AddBelieverInterface, view:ListBelieverInterface ):
        self.__init_var(model, addView, view)
        self.__configView()
        self.__actions()
        
    def __init_var(self, model: BelieverModel, addView: AddBelieverInterface, view: ListBelieverInterface):
        self.view = view
        self.addView = addView
        self.model = model
        self.func = Function()
        self.workerThread = None
        self.query = {'is_leader': '1'}
        self.fetchData(model.fetch_all(**self.query))
        self.family = []
        self.idEdit = 0
        self.isNewLead = False
        
    def __configView(self):
        self.labels = [
            'ID', 'Anarana', 'Fanampiny','Daty sy toerana nahaterahana',
            'Daty batisa', 'Daty sy toerana maha mpandray','Laharana karatra mpandray', 
            'Sampana sy/na Sampan\'asa','Andraikitra', 'Laharana finday']
        self.labelsFamily = [
            'ID', 'Anarana', 'Fanampiny','Lahy sa vavy','Amin\'ny fianakaviana', 'Daty sy toerana nahaterahana',
            'Daty batisa', 'Daty sy toerana maha mpandray','Laharana karatra mpandray', 
            'Sampana sy/na Sampan\'asa','Andraikitra', 'Laharana finday']
        self.setTableHeaderLabels(self.labels)
        self.addView.familyTableView.setHorizontalHeaderLabels(self.labelsFamily)
        
    def __actions(self):
        self.view.addAction.triggered.connect(lambda: self.addView.nParent.stackedWidget.setCurrentWidget(self.addView))
        self.view.exportAction.triggered.connect(lambda: self.exportExcel())
        self.addView.btnAdd.clicked.connect(self.addBeliver)
        self.addView.btnAddFamily.clicked.connect(self.addFamily)
        self.addView.btnClear.clicked.connect(self.clear)
        self.addView.familyTableView.contextMenuEvent = lambda e : self.tableFamilyRightClicked(e)
        self.view.tableView.contextMenuEvent = lambda e : self.tableRightClicked(e)
        self.addView.nParent.stackedWidget.currentChanged.connect(self.stackedOnChange)
    
    def stackedOnChange(self, pos):
        if self.idEdit != 0 and pos != 1:
            self.addView.clearLineEdit()
            self.addView.familyTableView.clearContents()
            self.family.clear()
            self.idEdit = 0
            self.isNewLead = False
        if self.idEdit == 0:
            self.addView.btnAdd.setText("Ampidirina")
            
    
    def clear(self):
        self.addView.clearLineEdit()
        self.addView.nParent.stackedWidget.setCurrentWidget(self.view)
        self.addView.familyTableView.clearContents()
        self.idEdit = 0
        self.isNewLead = False
    
    def tableRightClicked(self, event):
        selectedItems = self.view.tableView.selectedItems()
        if len(selectedItems) != 0:
            itemId = selectedItems[0].text()
            
            action = MenuAction(self)
            menu = RoundMenu(parent=self.view)
            menu.addAction(Action(FluentIcon.FOLDER, 'Jerena', triggered = lambda:action.show(itemId)))
            menu.addAction(Action(FluentIcon.EDIT, 'Ovaina', triggered = lambda: action.update(itemId)))
            menu.addSeparator()
            menu.addAction(Action(FluentIcon.DELETE, 'Fafana', triggered = lambda: action.confirmDelete(itemId)))

            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
        
    def tableFamilyRightClicked(self, event):
        selectedItems = self.addView.familyTableView.selectedIndexes()
        for i, item in enumerate(selectedItems):
            if i == 0:
                pos = item.row()
                menu = RoundMenu(parent=self.view)
                menu.addAction(Action(FluentIcon.EDIT, 'Ovaina', triggered= lambda: self.editFamily(pos)))
                menu.addAction(Action(FluentIcon.DELETE, 'Fafana', triggered= lambda: self.deleteFamily(pos)))
                self.posCur = QCursor().pos()
                cur_x = self.posCur.x()
                cur_y = self.posCur.y()
                menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
            
    def editFamily(self, pos):
        family:Believer = self.family[pos]
        dialog = AddBelieverDialog(self.addView.nParent)
        dialog.lastnameEdit.lineEdits[0].setText(family.lastname)
        dialog.firstnameEdit.lineEdits[0].setText(family.firstname)
        dialog.posFamilyCombox.combox.setCurrentIndex(0 if family.pos_family == "Zanaka" else 1)
        dialog.genderCombox.combox.setCurrentIndex(0 if family.gender == "Lahy" else 1)
        dialog.addressEdit.lineEdits[0].setText(family.address)
        dialog.regionEdit.lineEdits[0].setText(family.region)
        dialog.diaconEdit.lineEdits[0].setText(family.diacon)
        dialog.birthdayEdit.lineEdit.setDate(self.func.strToQDate(family.birthday))
        dialog.birthplaceEdit.lineEdit.setText(family.birthplace)
        dialog.dateBaptismDateEdit.lineEdit.setDate(self.func.strToQDate(family.date_of_baptism))
        dialog.placeBaptismEdit.lineEdit.setText(family.place_of_baptism)
        dialog.dateBaptismDateEdit.lineEdit.setDate(self.func.strToQDate(family.date_of_recipient))
        dialog.placeRecipientEdit.lineEdit.setText(family.place_of_recipient)
        dialog.numberRecipientEdit.lineEdit.setText(family.number_recipient)
        dialog.phoneEdit.lineEdits[0].setText(family.phone)
        dialog.deptWorkEdit.lineEdits[0].setText(family.dept_work)
        dialog.responsibilityEdit.lineEdits[0].setText(family.responsibility)
        dialog.yesButton.setText("Ovaina")
        if dialog.exec():
            believer = self.getBelieverFromDialog(dialog)
            believer['id'] = family.id
            #if believer.id == 0:
            self.family.pop(pos)
            self.family.insert(pos, believer)
            self.setData(self.addView.familyTableView, self.family)
            print(self.family)
    
    def getHeaderLabels(self, table):
        header_labels = []
        for col in range(table.columnCount()):
            item = table.horizontalHeaderItem(col)
            if item is not None:
                header_labels.append(item.text())
            else:
                header_labels.append("")
        return header_labels        
    
    def exportExcel(self):
        #print(self.view.parent.absInterface.tableView)
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self.view,"Avoaka",f"{os.path.expanduser('~')}","Excel File (*.xlsx)", options=options)
        db = self.func.getTableData(self.view.tableView)
        db.insert(0, self.getHeaderLabels(self.view.tableView))
        if fileName:
            self.func.writeExcelFile(fileName, base_de_donnees=db)
            os.startfile(fileName)
                
            
    def deleteFamily(self, pos):
        dialog = Dialog("Voulez vous le supprimer vraiment?", "Cette donnée sera perdu. Voulez-vous la supprimer vraiment?", self.addView.nParent)
        if dialog.exec():
            if self.idEdit != 0:
                self.model.delete_item(self.family[pos].id)
            self.family.pop(pos)
            self.setData(self.addView.familyTableView, self.family)
            
    def setIdMother(self, idFather):
        mothers : list[Believer] = self.model.fetch_all(id_conjoint=idFather)
        children : list[Believer] = self.model.fetch_all(id_father=idFather)
        for i, mother in enumerate(mothers):
            if i == 0:
                for child in children:
                    self.model.update_item(child.id, id_mother=str(mother.id))
        
    def addBeliver(self):
        w = self.addView
        lastname = w.lastnameEdit.lineEdit.text()
        firstname = w.firstnameEdit.lineEdit.text()
        address = w.addressEdit.lineEdit.text()
        region = w.regionEdit.lineEdit.text()
        diacon = w.diaconEdit.lineEdit.text()
        birthday = w.birthdayEdit.text()
        birthplace = w.birthplaceEdit.lineEdit.text()
        nameFather = w.nameFatherEdit.lineEdit.text()
        nameMother = w.nameMotherEdit.lineEdit.text()
        dateBaptism = w.baptismDateEdit.text()
        placeBaptism = w.baptismPlaceEdit.lineEdit.text()
        dateRecipient = w.recipientDateEdit.text()
        placeRecipient = w.recipientPlaceEdit.lineEdit.text()
        numberRecipient = w.recipientNumberEdit.lineEdit.text()
        phone = w.phoneEdit.lineEdit.text()
        deptWork = w.deptWorkEdit.lineEdit.text()
        responsability = w.responsibilityEdit.lineEdit.text()
        believer = Believer(
                lastname=lastname,
                firstname=firstname,
                is_leader=1,
                address=address,
                region=region,
                diacon=diacon,
                birthday=birthday,
                birthplace=birthplace,
                name_father=nameFather,
                name_mother=nameMother,
                date_of_baptism=dateBaptism,
                place_of_baptism=placeBaptism,
                date_of_recipient=dateRecipient,
                place_of_recipient=placeRecipient,
                number_recipient=numberRecipient,
                phone=phone,
                dept_work=deptWork,
                responsibility=responsability
            )
        if self.idEdit == 0:
            self.model.create(believer)
            allBelievers = self.model.fetch_all_items()
            lastBeliever : Believer = self.model.fetch_all_items()[len(allBelievers) - 1]
            for family in self.family:
                if family.pos_family == "Zanaka":
                    family['id_father'] = lastBeliever.id
                else:
                    family['id_conjoint'] = lastBeliever.id
                self.model.create(family)
            self.setIdMother(lastBeliever.id)
        else:
            obj = {}
            for field in dataclasses.fields(believer):
                if field.name != "id":
                    obj[field.name] = str(believer[field.name])
            if self.isNewLead:
                oldBeliever = self.model.fetch_item_by_id(str(self.idEdit))
                obj['is_leader'] = "1"
                obj['id_father'] = str(oldBeliever.id_father)
                obj['pos_family'] = str(oldBeliever.pos_family)
            self.model.update_item(self.idEdit, **obj)
            
            for family in self.family:
                if family.pos_family == "Zanaka":
                    family['id_father'] = self.idEdit
                else:
                    family['id_conjoint'] = self.idEdit
                blv = self.model.fetch_all(id=family.id)
                if len(blv) == 0:
                    self.model.create(family)
                else:
                    obj = {}
                    for field in dataclasses.fields(family):
                        if field.name != "id":
                            obj[field.name] = str(family[field.name])
                    self.model.update_item(family.id, **obj)
            self.setIdMother(self.idEdit)
                    
            
        self.fetchData(self.model.fetch_all(**self.query))
        self.addView.clearLineEdit()
        self.addView.familyTableView.clearContents()
        self.addView.nParent.stackedWidget.setCurrentWidget(self.view)
        self.idEdit = 0
        self.isNewLead = False
        
    def getBelieverFromDialog(self, w):
            lastname = w.lastnameEdit.text(0)
            firstname = w.firstnameEdit.text(0)
            posFamily = w.posFamilyCombox.combox.currentText()
            gender = w.genderCombox.combox.currentText()
            address = w.addressEdit.text(0)
            region = w.regionEdit.text(0)
            diacon = w.diaconEdit.text(0)
            birthday = w.birthdayEdit.text()
            birthplace = w.birthplaceEdit.lineEdit.text()
            '''nameFather = w.nameFatherEdit.text(0)
            nameMother = w.nameMotherEdit.text(0)'''
            dateBaptism = w.dateBaptismDateEdit.text()
            placeBaptism = w.placeBaptismEdit.lineEdit.text()
            dateRecipient = w.dateRecipientDateEdit.text()
            placeRecipient = w.placeRecipientEdit.lineEdit.text()
            numberRecipient = w.numberRecipientEdit.lineEdit.text()
            phone = w.phoneEdit.text(0)
            deptWork = w.deptWorkEdit.text(0)
            responsability = w.responsibilityEdit.text(0)
            
            return Believer(
                lastname=lastname,
                firstname=firstname,
                gender=gender,
                pos_family=posFamily,
                address=address,
                region=region,
                diacon=diacon,
                birthday=birthday,
                birthplace=birthplace,
                date_of_baptism=dateBaptism,
                place_of_baptism=placeBaptism,
                date_of_recipient=dateRecipient,
                place_of_recipient=placeRecipient,
                number_recipient=numberRecipient,
                phone=phone,
                dept_work=deptWork,
                responsibility=responsability
            )
        
                
    def addFamily(self):
        w = AddBelieverDialog(self.view.nParent)
        adrss = self.addView.addressEdit.lineEdit.text()
        rgn = self.addView.regionEdit.lineEdit.text()
        w.addressEdit.lineEdits[0].setText(adrss)
        w.regionEdit.lineEdits[0].setText(rgn)
        if w.exec():
            believer = self.getBelieverFromDialog(w)
            self.family.append(believer)
            '''["", lastname, firstname, gender, posFamily, f'{birthday} {birthplace}', deptWork, dateBaptism, placeBaptism,
                 dateRecipient, placeRecipient, numberRecipient, deptWork, responsability]
            )'''
            self.setData(self.addView.familyTableView, self.family)
            #self.model.create(believer)
            #self.fetchData(self.model.fetch_all())
    def setData(self, table, believers: list[Believer]):
        data = []
        for i, believer in enumerate(believers):
            data.append([believer.id, believer.lastname, believer.firstname, believer.gender, believer.pos_family, 
                         f'{believer.birthday} {believer.birthplace}', believer.date_of_baptism, 
                         believer.place_of_baptism, believer.date_of_recipient, believer.place_of_recipient, 
                         believer.number_recipient, "", believer.responsibility])
        table.setData(data)
    
    def fetchData(self, data):
        self.view.progressBar.setVisible(True)
        self.actionWorkerThread(data)
        
    def setTableHeaderLabels(self, headerLabels: list):
        self.view.tableView.setHorizontalHeaderLabels(headerLabels)
        
    def actionWorkerThread(self, data):
        if self.workerThread is None or not self.workerThread.isRunning():
            self.workerThread = QThread()
            self.worker = DatabaseWorker(data)
            self.worker.moveToThread(self.workerThread)
            self.workerThread.started.connect(self.worker.run)
            self.worker.progress.connect(self.updateProgress)
            self.worker.result.connect(self.handleResult)
            self.worker.finished.connect(self.workerThread.quit)
            self.workerThread.start()
        else:
            self.workerThread.quit()
    
    def updateProgress(self, progress):
        self.view.progressBar.setValue(int(progress))
        
    def handleResult(self, data:list[Believer]):
        self.view.progressBar.setVisible(False)
        self.view.progressBar.setValue(0)
        self.workerThread.quit()
        dataList = []
        for item in data:
            dataList.append([item.id, item.lastname, item.firstname,f'{item.birthday} {item.birthplace}', 
                   item.date_of_baptism,f'{item.date_of_recipient} {item.place_of_recipient}', 
                   item.number_recipient,item.dept_work, item.responsibility, item.phone])
        self.view.tableView.setData(dataList)
        
    def setTableContextMenu(self, contextMenu):
        self.view.tableView.contextMenuEvent = lambda event: contextMenu(event)