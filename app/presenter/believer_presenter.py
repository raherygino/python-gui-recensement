from PyQt5.QtCore import QThread, QPoint
from ..models import DatabaseWorker, BelieverModel, Believer
from ..view import ListBelieverInterface, AddBelieverDialog, AddBelieverInterface

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
        self.fetchData(model.fetch_all())
        
    def __configView(self):
        self.setTableHeaderLabels([
            'ID', 'Anarana', 'Fanampiny','Daty sy toerana nahaterahana', 'Asa', 
            'Daty batisa', 'Daty sy toerana maha mpandray','Laharana karatra mpandray', 
            'Sampana sy/na Sampan\'asa','Andraikitra', 'Laharana finday'])
        
    def __actions(self):
        self.view.addAction.triggered.connect(self.addBielever)
        self.addView.btnAddFamily.clicked.connect(self.addBielever)
        
    def addBielever(self):
        w = AddBelieverDialog(self.view.nParent)
        if w.exec():
            lastname = w.lastnameEdit.text(0)
            firstname = w.firstnameEdit.text(0)
            address = w.addressEdit.text(0)
            region = w.regionEdit.text(0)
            diacon = w.diaconEdit.text(0)
            birthday = w.birthdayEdit.text(0)
            birthplace = w.birthdayEdit.text(1)
            nameFather = w.nameFatherEdit.text(0)
            nameMother = w.nameMotherEdit.text(0)
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
            self.fetchData(self.model.fetch_all())
    
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