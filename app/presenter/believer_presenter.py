from PyQt5.QtCore import QThread, QPoint
from PyQt5.QtGui import QCursor
from qfluentwidgets import FluentIcon, RoundMenu, MenuAnimationType, Action
from ..models import DatabaseWorker, BelieverModel, Believer
from ..view import ListBelieverInterface, AddBelieverDialog, AddBelieverInterface, ShowBelieverDialog

class BelieverPresenter:
    
    def __init__(self, model: BelieverModel, addView: AddBelieverInterface, view:ListBelieverInterface ):
        self.__init_var(model, addView, view)
        self.__configView()
        self.__actions()
        
    def __init_var(self, model: BelieverModel, addView: AddBelieverInterface, view: ListBelieverInterface):
        self.view = view
        self.addView = addView
        self.model = model
        self.workerThread = None
        self.query = {'pos_family': 'Loha-mpianakaviana'}
        self.fetchData(model.fetch_all(**self.query))
        self.family = []
        
    def __configView(self):
        self.labels = [
            'ID', 'Anarana', 'Fanampiny','Daty sy toerana nahaterahana', 'Asa', 
            'Daty batisa', 'Daty sy toerana maha mpandray','Laharana karatra mpandray', 
            'Sampana sy/na Sampan\'asa','Andraikitra', 'Laharana finday']
        self.labelsFamily = [
            'ID', 'Anarana', 'Fanampiny','Lahy sa vavy','Amin\'ny fianakaviana', 'Daty sy toerana nahaterahana', 'Asa',
            'Daty batisa', 'Daty sy toerana maha mpandray','Laharana karatra mpandray', 
            'Sampana sy/na Sampan\'asa','Andraikitra', 'Laharana finday']
        self.setTableHeaderLabels(self.labels)
        self.addView.familyTableView.setHorizontalHeaderLabels(self.labelsFamily)
        
    def __actions(self):
        #self.view.addAction.triggered.connect(self.addBielever)
        self.addView.btnAdd.clicked.connect(self.addBeliver)
        self.addView.btnAddFamily.clicked.connect(self.addFamily)
        self.addView.familyTableView.contextMenuEvent = lambda e : self.tableFamilyRightClicked(e)
        self.view.tableView.contextMenuEvent = lambda e : self.tableRightClicked(e)
    
    def tableRightClicked(self, event):
        selectedItems = self.view.tableView.selectedItems()
        if len(selectedItems) != 0:
            itemId = selectedItems[0].text()
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
            dialog.table.setHorizontalHeaderLabels(self.labelsFamily)
            
            for i, row in enumerate(allRows):
                for j, column in enumerate(row):
                    dialog.addLabelValue(column[0], column[1], i,j)
                    
            data = self.model.fetch_all(id_conjoint=itemId)
            for value in self.model.fetch_all(id_father=itemId):
                data.append(value)
                
            self.setData(dialog.table, data)
            dialog.exec()
        
    def tableFamilyRightClicked(self, event):
        selectedItems = self.addView.familyTableView.selectedItems()
        if (len(selectedItems) != 0):
            idItem = selectedItems[0].text()
            menu = RoundMenu(parent=self.view)
            menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered= lambda: self.deleteFamily(selectedItems)))

            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
            
    def deleteFamily(self, items):
        self.family.pop(int(items[0].text()))
        self.setData(self.family)
        
    def addBeliver(self):
        w = self.addView
        lastname = w.lastnameEdit.lineEdit.text()
        firstname = w.firstnameEdit.lineEdit.text()
        address = w.addressEdit.lineEdit.text()
        region = w.regionEdit.lineEdit.text()
        diacon = w.diaconEdit.lineEdit.text()
        birthday = w.birthdayEdit.lineEdit.text()
        birthplace = w.birthdayEdit.lineEdit.text()
        nameFather = w.nameFatherEdit.lineEdit.text()
        nameMother = w.nameMotherEdit.lineEdit.text()
        dateBaptism = w.baptismDateEdit.lineEdit.text()
        placeBaptism = w.baptismPlaceEdit.lineEdit.text()
        dateRecipient = w.recipientDateEdit.lineEdit.text()
        placeRecipient = w.recipientPlaceEdit.lineEdit.text()
        numberRecipient = w.recipientNumberEdit.lineEdit.text()
        phone = w.phoneEdit.lineEdit.text()
        deptWork = w.deptWorkEdit.lineEdit.text()
        responsability = w.responsibilityEdit.lineEdit.text()
        believer = Believer(
                lastname=lastname,
                firstname=firstname,
                pos_family="Loha-mpianakaviana",
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
        
        self.model.create(believer)
        allBelievers = self.model.fetch_all_items()
        lastBeliever : Believer = self.model.fetch_all_items()[len(allBelievers) - 1]
        for family in self.family:
            if family.pos_family == "Zanaka":
                family['id_father'] = lastBeliever.id
            else:
                family['id_conjoint'] = lastBeliever.id
            self.model.create(family)
        self.fetchData(self.model.fetch_all(**self.query))
                
    def addFamily(self):
        w = AddBelieverDialog(self.view.nParent)
        if w.exec():
            lastname = w.lastnameEdit.text(0)
            firstname = w.firstnameEdit.text(0)
            posFamily = w.posFamilyCombox.combox.currentText()
            gender = w.genderCombox.combox.currentText()
            address = w.addressEdit.text(0)
            region = w.regionEdit.text(0)
            diacon = w.diaconEdit.text(0)
            birthday = w.birthdayEdit.text(0)
            birthplace = w.birthdayEdit.text(1)
            '''nameFather = w.nameFatherEdit.text(0)
            nameMother = w.nameMotherEdit.text(0)'''
            dateBaptism = w.baptismEdit.text(0)
            placeBaptism = w.baptismEdit.text(1)
            dateRecipient = w.recipientEdit.text(0)
            placeRecipient = w.recipientEdit.text(1)
            numberRecipient = w.recipientEdit.text(2)
            phone = w.phoneEdit.text(0)
            deptWork = w.deptWorkEdit.text(0)
            responsability = w.responsibilityEdit.text(0)
            
            believer = Believer(
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
            data.append([str(i), believer.lastname, believer.firstname, believer.gender, believer.pos_family, 
                         f'{believer.birthday} {believer.birthplace}', believer.dept_work, believer.date_of_baptism, 
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
            dataList.append([item.id, item.lastname, item.firstname,f'{item.birthday} ,{item.birthplace}', '', 
                   item.date_of_baptism,f'{item.date_of_recipient} {item.place_of_recipient}', 
                   item.number_recipient,item.dept_work, item.responsibility, item.phone])
        self.view.tableView.setData(dataList)
        
    def setTableContextMenu(self, contextMenu):
        self.view.tableView.contextMenuEvent = lambda event: contextMenu(event)