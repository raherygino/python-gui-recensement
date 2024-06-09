from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFileDialog
from qfluentwidgets import RoundMenu, Action, FluentIcon, MessageBox, MenuAnimationType

from ...common import Function, Utils
from ...view import StudentsInterface, NewStudentDialog, NewSubjectDialog
from ...models import StudentModel, Student,SubjectModel, Subject

from .db_presenter import StudentDbPresenter
from .eap_presenter import EapPresenter
from .eip_presenter import EipPresenter

import os

class StudentsPresenter:
    
    def __init__(self, view:StudentsInterface, model:StudentModel):
        self.view = view
        self.model = model
        self.modelSubject = SubjectModel()
        self.func = Function()
        self.timer = QTimer()
        self.utils = Utils()
        self.__init_presenter()
        self.__actions()
        
    def __init_presenter(self):
        self.dbPresenter = StudentDbPresenter(self)
        self.eipPresenter = EapPresenter(self)
        self.eapPresenter = EipPresenter(self)
        
    def __actions(self):
        self.view.refreshAction.triggered.connect(lambda: self.view.nParent.currentPromotion.emit(self.promotionId))
        self.view.importAction.triggered.connect(lambda : self.importData())
        self.view.deleteAction.triggered.connect(lambda : self.deleteAll())
        self.view.exportAction.triggered.connect(lambda : self.exportData())
        self.view.exportActionCsv.triggered.connect(lambda: self.exportCsv())
        self.view.nParent.currentPromotion.connect(lambda currentId : self.setPromotionId(currentId))
        self.view.addSubject.triggered.connect(lambda: self.showDialogSubject())
        #self.view.addComp.triggered.connect(lambda: self.addComp())
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
            number=matricule[2:4]
        )
        
    def showDialogSubject(self):
        dialog = NewSubjectDialog(self.view)
        dialog.yesBtn.clicked.connect(lambda: self.getTableDialogData(dialog))
        dialog.exec()
    
    def getTableDialogData(self, dialog):
        table = dialog.table
        row_count = table.rowCount()
        column_count = table.columnCount()

        table_data = []
        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                item = table.item(row, column)
                if item is not None:
                    row_data.append(item.text())
            if len(row_data) != 0:
                table_data.append(row_data)
                
        abrv = []
        isDuplicate = False
        for item in table_data:
            abrv.append(item[0])
            if self.is_duplicate(item[0], abrv):
                isDuplicate = True
        
        if isDuplicate:
            self.utils.infoBarError("Erreur", "Une matière est reproduite en double.", dialog)
        else:
            if len(table_data) == 0:
                self.utils.infoBarError("Vide!", "Vous n'avez ajouté aucune matière!", dialog)
            else:
                for item in table_data:
                    self.modelSubject.create(Subject(promotion_id=self.promotionId, abrv=item[0], title=item[0]))
                dialog.close()
                self.utils.infoBarSuccess("Ajouté", "Matières ajoutés avec succès", self.view)
                
    def is_duplicate(self, item, lst):
        return lst.count(item) > 1
        
    def createComp(self, dialog, dataCombox):
        name = dialog.nameLineEdit.text()
        abr = dialog.abrLineEdit.text()
        ''''comp = Comportement(
                promotion_id=self.promotionId,
                name=name,
                abrv=abr,
                comp_type=dataCombox[dialog.typeCombox.currentIndex()])
        if self.compModel.check(comp, "name") == 0:
            self.compModel.create(comp)
            self.refreshCompTable(dialog.table)
            dialog.nameLineEdit.setText("")
            dialog.abrLineEdit.setText("")
            self.func.toastSuccess("Ajout avec succès", "", self.view)
        else:
            self.func.errorSuccess("Nom existe déjà", "Le nom que vous avez choisi existe déjà", self.view)'''
            
    def addComp(self):
        dialog = NewSubjectDialog(self.view)
        ''''typeComp = self.typeCompModel.fetch_items_by_id(0)
        dataCombox = []
        for val in typeComp:
            dataCombox.append(val.name)
        dialog.typeCombox.addItems(dataCombox)
        self.refreshCompTable(dialog.table)
        dialog.btnAdd.clicked.connect(lambda: self.createComp(dialog, dataCombox))
        dialog.yesButton.setText("Ok")
        dialog.cancelButton.setVisible(False)'''
        dialog.exec()
    
    def refreshCompTable(self, table):
        ids = []
        data = []
        '''for comp in self.compModel.fetch_items_by_id(self.promotionId):
            data.append([comp.name, comp.comp_type])
            ids.append(comp.id)
        table.setData(data)'''
        table.contextMenuEvent = lambda  event, table = table, ids=ids : self.rightClickCompTable(event,table, ids)
        
    def rightClickCompTable(self, event, table, ids):
        
            menu = RoundMenu(parent=self.view)
            menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered=lambda:self.deleteMove(ids[table.currentRow()], table)))
            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()

            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
            
    def deleteMove(self, id, table):
        dialog = MessageBox('Supprimer', "Voulez vous le supprimer?", self.view)
        if dialog.exec():
            #self.compModel.delete_item(id)
            self.refreshCompTable(table)
        
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
            
        '''elif currentTab == 1:
            data = self.modelMove.search_query(query, matricule=text, student=text)
            if len(text) < 3:
                data = self.absPresenter.defaultData
            self.absPresenter.fetchData(data)'''
        
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
        #print(self.view.parent.absInterface.tableView)
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self.view,"Exporter",f"{os.path.expanduser('~')}","Excel File (*.xlsx)", options=options)
        db = self.func.getTableData(self.dbPresenter.view.tableView)
        db.insert(0, self.getHeaderLabels(self.dbPresenter.view.tableView))
        
        dAbs = self.func.getTableData(self.absPresenter.view.tableView)
        dAbs.insert(0, self.getHeaderLabels(self.absPresenter.view.tableView))
        
        dDay = self.func.getTableData(self.dayPresenter.view.tableView)
        dDay.insert(0, self.getHeaderLabels(self.dayPresenter.view.tableView))
        
        if fileName:
            
            self.func.writeExcelFile(fileName, base_de_donnees=db, grille_d_abscence=dAbs, total_nombre_de_jour=dDay)
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
            with open(filename, "r") as data: 
                listStudent = []
                for line in data:
                    items = line.strip().split(";")
                    matricule = items[0]
                    level = items[1]
                    #FOR PROMOTION SANDRATRA
                    level = "EAP"
                    if matricule.find("11") == 0 or \
                        matricule.find("12") == 0 or \
                        matricule.find("21") == 0 or \
                        matricule.find("31") == 0:
                        level = "EIP"
                    name = items[2].split(" ")
                    lastname = name[0]
                    firstname = ' '.join([val for val in name[1:]]) if len(name) > 1 else ""
                    genre = items[3]
                    listStudent.append(Student(
                        promotion_id=self.promotionId,
                        lastname=lastname,
                        firstname=firstname,
                        gender=genre,
                        level=level,
                        matricule=matricule,
                        company=matricule[0],
                        section=matricule[1],
                        number=matricule[2:4]
                    ))
                self.model.create_multiple(listStudent)
                self.view.nParent.currentPromotion.emit(self.promotionId)
                
    def deleteAll(self):
        currentTab = self.view.stackedWidget.currentIndex()
        if currentTab == 0 or currentTab == 2:
            dialog = MessageBox('Supprimer', "Voulez vous le supprimer?", self.view.nParent)
            if dialog.exec():
                self.model.delete_by(promotion_id = self.promotionId)
                self.view.nParent.refresh.emit(["mouvement"])
                self.dbPresenter.setPromotionId(self.promotionId)
        elif currentTab == 1:
            dialog = MessageBox('Supprimer', "Voulez vous le supprimer?", self.view.nParent)
            if dialog.exec():
                #self.modelMove.delete_by(promotion_id = self.promotionId)
                self.view.nParent.refresh.emit(["mouvement"])