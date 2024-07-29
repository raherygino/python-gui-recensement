from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

from ...components import ImportDialog, ConfirmDialog, BigDialog
from ...common import Function, Utils
from ...view import StudentsInterface, NewStudentDialog, NewSubjectDialog
from ...models import StudentModel, Student,SubjectModel, Subject, MarkModel

from .db_presenter import StudentDbPresenter
from .eap_presenter import EapPresenter
from .eip_presenter import EipPresenter

import os

class StudentsPresenter:
    
    def __init__(self, view:StudentsInterface, model:StudentModel):
        self.view = view
        self.model = model
        self.modelSubject = SubjectModel()
        self.modelMark = MarkModel()
        self.func = Function()
        self.timer = QTimer()
        self.utils = Utils()
        
        self.__init_presenter()
        self.__actions()
        
    def __init_presenter(self):
        self.dbPresenter = StudentDbPresenter(self)
        self.eipPresenter = EipPresenter(self)
        self.eapPresenter = EapPresenter(self)
        
    def __actions(self):
        self.view.refreshAction.triggered.connect(lambda: self.view.nParent.currentPromotion.emit(self.promotionId))
        self.view.importAction.triggered.connect(lambda : self.importData())
        self.view.deleteAction.triggered.connect(lambda : self.deleteAll())
        self.view.exportAction.triggered.connect(lambda : self.exportData())
        self.view.exportActionCsv.triggered.connect(lambda: self.exportCsv())
        self.view.nParent.currentPromotion.connect(lambda currentId : self.setPromotionId(currentId))
        self.view.addSubject.triggered.connect(lambda: self.showDialogSubject())
        self.view.addAction.triggered.connect(lambda: self.addStudent())
        self.view.searchLineEdit.textChanged.connect(self.onSearch)
        self.view.searchLineEdit.returnPressed.connect(self.search)
        self.view.searchLineEdit.searchButton.clicked.connect(self.search)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.search)
    
    def setPromotionId(self, promotionId):
        self.promotionId = promotionId
    
    def addStudent(self):
        dialog = NewStudentDialog(self.view.nParent)
        if dialog.exec():
            student = self.dataStudentFromDialog(dialog)
            if len(self.model.fetch_all(promotion_id=self.promotionId, matricule=student.matricule)) == 0:
                self.model.create(student)
                self.dbPresenter.setPromotionId(self.promotionId)
                self.view.nParent.refresh.emit(["mouvement"])
            else:
                self.func.errorSuccess("Matricule invalide", "Matricule exist déjà", self.view.nParent)
    
    def dataStudentFromDialog(self, dialog):
        lastname = dialog.lastnameEdit.lineEdit(0).text()
        firstname = dialog.firstnameEdit.lineEdit(0).text()
        matricule = dialog.matriculeEdit.lineEdit(0).text()
        level = dialog.gradeEdit.value()
        gender = dialog.genderEdit.value()
        return Student(
            promotion_id=self.promotionId,
            lastname=lastname,
            firstname=firstname,
            gender=gender,
            level=level,
            matricule=matricule,
            company=matricule[0],
            section=matricule[1],
            number=matricule[2:4])
        
    def showDialogSubject(self):
        dialog = NewSubjectDialog(self.view)
        subjects:list[Subject] = self.modelSubject.fetch_all(promotion_id=self.promotionId, level=self.getLevel())
        allSbjcts = []
        for subject in subjects:
            allSbjcts.append([subject.id, subject.abrv, subject.title, subject.coef])
        dialog.count.spinbox.setValue(len(subjects))
        dialog.table.setRowCount(len(subjects))
        dialog.table.setData(allSbjcts)
        dialog.table.setColNoEditable(0)
        dialog.btnExport.clicked.connect(lambda: self.exportSubject(dialog))
        dialog.btnImport.clicked.connect(lambda: self.importSubject(dialog))
        dialog.yesBtn.clicked.connect(lambda: self.getTableDialogData(dialog))
        dialog.exec()
        
    def exportSubject(self, dialog: NewStudentDialog):
        data = dialog.table.getData()
        if len(data) > 0:
            destination_path, _ = QFileDialog.getSaveFileName(self.view, "Exporter", "", "All Files (*);;Text Files (*.csv)")
            if destination_path:
                with open(destination_path, 'w') as f:
                    for item in data:
                        line = ";".join([nItem for nItem in item])
                        f.writelines(f'{line}\n')
        else:
            self.utils.infoBarError('Erreur', "Aucune donnée à exporter", self.view)
        
    def importSubject(self, dialog: NewStudentDialog):
        destination_path, _ = QFileDialog.getOpenFileName(self.view, "Exporter", "", "CSV File (*.csv)")
        if destination_path:
            lenData = len(dialog.table.getData())
            with open(destination_path, 'r') as f:
                data = []
                for i, line in enumerate(f):
                    i = lenData + i
                    nLine = line.replace("\n", "").split(";")
                    data.append(nLine)
                
                dialogImport = ImportDialog(data, dialog.table.getHorizontalLabels(), dialog)
                dialogImport.yesBtn.clicked.connect(lambda:  self.addSubToTable(ImportDialog, dialog))
                dialogImport.exec()
                    
    def addSubToTable(self, dialogImport: ImportDialog, dialog):
        nData = dialogImport.getData()
        first =  []
        for nItem in nData[0]:
            if nItem != None:
                first.append(nItem)
        if len(first) == 0:
            self.utils.infoBarError('Erreur', 'Aucune données n\'a été choisi!', dialog)
        else:
            for i, item in enumerate(nData):
                dialog.table.insertRow(i)
                for j, nItem in enumerate(item):
                    qWidget = QTableWidgetItem(nItem)
                    dialog.table.setItem(i, j, qWidget)
            dialogImport.accept()
                
    def getTableDialogData(self, dialog):
        data = dialog.table.getData()
        dataSubject = []
        for item in data:
            subject = Subject(
                id=item[0] if item[0] != "" else 0, 
                promotion_id=self.promotionId, 
                abrv=item[1], 
                title=item[2], 
                coef=item[3] if item[3] != "" else 1,  
                level=self.getLevel())
            dataSubject.append(subject)
        self.create(dataSubject, dialog)
            
    def create(self, table_data, dialog):
        isValid = True
        message = ""
        abrv = [subject.abrv for subject in table_data]
        for subject in table_data:
            if not subject.abrv:
                message = "Une matière doit avoir une abréviation"
                isValid = False
            if not subject.title:
                message = "Une matière doit avoir un titre"
                isValid = False
            if abrv.count(subject.abrv) > 1:
                message = "Une matière doit être répéter plusieurs fois"
                isValid = False
                
        if isValid:
            subjInDb = [item.id  for item in self.modelSubject.fetch_all(promotion_id=self.promotionId, level=self.getLevel())]
            subjInDial = [int(item.id)  for item in table_data]
            subjDeleted = [item for item in subjInDb if item not in subjInDial]
            for subj in subjDeleted:
                self.modelSubject.delete_item(subj)

            for item in table_data:
                sub = {
                    "abrv":  item.abrv,
                    "title": item.title,
                    "coef":  item.coef 
                }
                if item.id == 0:
                    self.modelSubject.create(item)
                else:
                    self.modelSubject.update_item(item.id, **sub)
            dialog.close()
            self.utils.infoBarSuccess("Mise à jour", "Mis à jour avec succés", self.view)
            self.view.nParent.subjectRefresh.emit(self.getLevel())
        else:
            self.utils.infoBarError("Erreur", message, dialog)
            
    def getLevel(self) -> str:
        level = "EIP"
        if self.view.stackedWidget.currentIndex() == 2:
            level = "EAP"
        return level
                
    def is_duplicate(self, item, lst):
        return lst.count(item) > 1
        
    def onSearch(self, text):
        currentTab = self.view.stackedWidget.currentIndex()
        if len(text) > 2:
            self.timer.start()
        else:
            presenter = self.dbPresenter
            if currentTab == 1 :
                presenter = self.absPresenter
            presenter.handleResult(presenter.defaultData)
        
    def search(self):
        text = self.view.searchLineEdit.text()
        currentTab = self.view.stackedWidget.currentIndex()
        query = {"promotion_id":self.promotionId}
        
        if currentTab == 0:
            data = self.model.search_query(query, matricule=text, firstname=text, lastname=text)
            if len(text) < 3:
                data = self.dbPresenter.defaultData
            self.dbPresenter.fetchData(data)
            
        self.timer.stop()
    
    def getHeaderLabels(self, table):
        header_labels = []
        for col in range(table.columnCount()):
            item = table.horizontalHeaderItem(col)
            if item is not None:
                header_labels.append(item.text())
            else:
                header_labels.append("")
        return header_labels
    
    
    def exportData(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self.view,"Exporter",f"{os.path.expanduser('~')}","Excel File (*.xlsx)", options=options)
        db = self.func.getTableData(self.dbPresenter.view.tableView)
        db.insert(0, self.getHeaderLabels(self.dbPresenter.view.tableView))
        
        dEip = self.func.getTableData(self.eipPresenter.view.tableView)
        dEip.insert(0, self.getHeaderLabels(self.eipPresenter.view.tableView))
        
        dEap = self.func.getTableData(self.eapPresenter.view.tableView)
        dEap.insert(0, self.getHeaderLabels(self.eapPresenter.view.tableView))
        
        if fileName:
            
            self.func.writeExcelFile(fileName, base_de_donnees=db, EIP=dEip, EAP=dEap)
            os.startfile(fileName)
    
    def exportCsv(self):
        data = ""
        items:list[Student] = self.model.fetch_all(promotion_id=self.promotionId)
        for item in items:
            data += f"{item.matricule};{item.level};{item.lastname} {item.firstname};{item.gender};\n"
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self.view,"Exporter",f"{os.path.expanduser('~')}","CSV File (*.csv)", options=options)
        if fileName:
            self.saveFile(data, fileName)
    
    def saveFile(self, data, filename):
        with open(filename, "w") as file:
            file.write(data)
        os.startfile(filename)
                        
    def importData(self):
        filename = self.func.importFile(self.view, "Importer base de données", "CSV File (*.csv)")
        if filename:
            with open(filename, 'r') as f:
                data = []
                for i, line in enumerate(f):
                    nLine = line.replace("\n", "").split(";")
                    data.append(nLine)
                dialogImport = ImportDialog(data, ['Matricule', 'Grade', 'Nom et prénoms', 'Genre'], self.view.nParent)
                dialogImport.yesBtn.clicked.connect(lambda:  self.addDataImported(ImportDialog))
                dialogImport.exec()
                    
    def addDataImported(self, dialog:ImportDialog):
        data = dialog.getData()
        matricule  = data[0][0]
        if matricule == None:
            self.utils.infoBarError('', 'Vous  n\'avez pas choisi le colonne matricule', dialog)
        else:
            listStudent =  []
            for item in data:
                name = item[2].split(" ")
                lastname = name[0]
                firstname = ' '.join([val for val in name[1:]]) if len(name) > 1 else ""
                listStudent.append(
                    Student(
                        promotion_id = self.promotionId,
                        matricule    = item[0],
                        company      = item[0][0],
                        section      = item[0][1],
                        number       = item[0][2:4],
                        firstname    = firstname,
                        lastname     = lastname,
                        gender       = item[3],
                        level        = item[1]
                    ))
            self.model.create_multiple(listStudent)
            dialog.accept()
            self.view.nParent.currentPromotion.emit(self.promotionId)  
        
    def deleteAll(self):
        dialog = BigDialog(self.view)
        dialog.exec()
        '''currentTab = self.view.stackedWidget.currentIndex()
        if currentTab == 0 or currentTab == 2:
            dialog = ConfirmDialog('Supprimer', "Voulez vous le supprimer?", self.view.nParent)
            if dialog.exec():
                self.model.delete_by(promotion_id = self.promotionId)
                self.modelMark.delete_by(promotion_id = self.promotionId)
                self.view.nParent.refresh.emit(["mouvement"])
                self.view.nParent.currentPromotion.emit(self.promotionId)
        elif currentTab == 1:
            dialog = ConfirmDialog('Supprimer', "Voulez vous le supprimer?", self.view.nParent)
            if dialog.exec():
                self.view.nParent.refresh.emit(["mouvement"])'''