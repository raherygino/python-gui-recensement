from PyQt5.QtCore import QPoint, QThread
from PyQt5.QtGui import QCursor 

from ...view import DatabaseStudentTab
from ...models import StudentModel, DatabaseWorker, SubjectModel, MarkModel
from ...components import PopupTeachingTip, TeachingTipTailPosition, FilterFlyoutView
from ...common.constants import *

class BaseStudentPresenter:
    
    def __init__(self, view, parent):
        self.__init_needly_var(view, parent)
        self.__init_widget()
        self.__init_var()
        self.workerThread = None
        self.__actions()
        
    def __init_needly_var(self, view, parent):
        self.view:DatabaseStudentTab = view
        self.model:StudentModel = parent.model
        self.modelSubject = parent.modelSubject
        self.modelMark = MarkModel()
        
        self.mainView = self.view.parent.nParent
        self.parent = parent
        self.labels = [
            LABEL.MATRICULE, LABEL.GRADE, LABEL.COMPANY, LABEL.SECTION, 
            LABEL.LASTNAME,LABEL.FIRSTNAME, LABEL.GENDER]
        
    def __init_widget(self):
        self.view.tableView.contextMenuEvent = lambda event: self.mouseRightClick(event)
        self.view.tableView.setHorizontalHeaderLabels(self.labels)
        self.view.tableView.horizontalHeader().sectionClicked.connect(lambda index: self.showFilterTip(index))
        
    def __init_var(self):
        self.promotionId = 0
        self.companyStudents = 0
        self.sectionStudents = 0
        self.day = 0
        self.query = {"promotion_id":self.promotionId}
        
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
        
    def __actions(self):
        self.mainView.currentPromotion.connect(lambda currentId : self.setPromotionId(currentId))
        
    def setPromotionId(self, promotionId):
        self.promotionId = promotionId
        self.query = {"promotion_id":promotionId}
        self.defaultData = self.model.fetch_all(**self.query)
        self.fetchData(self.defaultData)
    
    def setLabelIntoTable(self,promotionId, level):
        subjects = self.modelSubject.fetch_all(promotion_id=promotionId, level=level)
        labels = []
        labels.extend(self.labels)
        labels.extend([subject.abrv for subject in subjects])
        labels.extend([f'{subject.abrv}\ncoef' for subject in subjects])
        self.view.tableView.setHorizontalHeaderLabels(labels)
        
    def intColFilter(self):
        self.companyStudents = self.fetchDataGroup(self.model, key="company", label=LABEL.COMPANY)
        self.sectionStudents = self.fetchDataGroup(self.model, key="section", label=LABEL.SECTION)
        self.levelStudents = self.fetchDataGroup(self.model, key="level")
        self.genderStudents = self.fetchDataGroup(self.model, key="gender")
        #self.motifsMove = self.fetchDataGroup(self.modelMove, key="motif")
        #self.obsMove = self.fetchDataGroup(self.modelMove, key="subType")
        self.day = list(map(str, self.fetchDataGroup(self.model, key="day")))
        
    def fetchData(self, data):
        self.view.progressBar.setVisible(True)
        self.intColFilter()
        self.actionWorkerThread(data)
        
    def fetchDataGroup(self, model, **kwargs):
        data = []
        for item in model.fetch_all(promotion_id=self.promotionId, group=kwargs.get("key")):
            if "label" in kwargs.keys():
                data.append(self.setLabelValue(item[kwargs.get("key")], kwargs.get("label")))
            else:
                data.append(item[kwargs.get("key")])
        return data
    
    def mouseRightClick(self, event):
        selectedItems = self.view.tableView.selectedItems()
        if (len(selectedItems) != 0):
            matricule_item = self.view.tableView.selectedItems()[0].text()
            #action = MenuAction(self)
            '''menu = RoundMenu(parent=self.view)
            menu.addAction(Action(FluentIcon.FOLDER, 'Voir', triggered = lambda:action.show(matricule_item)))
            menu.addAction(Action(FluentIcon.EDIT, 'Modifier', triggered = lambda: action.update(matricule_item)))
            menu.addSeparator()
            menu.addAction(Action(FluentIcon.SCROLL, 'Mouvement', triggered = lambda: action.mouvement(matricule_item)))
            menu.addSeparator()
            menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda: action.delete(matricule_item)))
            menu.menuActions()[-2].setCheckable(True)
            menu.menuActions()[-2].setChecked(True)

            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)'''
        
    def updateProgress(self, progress):
        self.view.progressBar.setValue(int(progress))
        
    def handleResult(self, data:list):
        self.view.progressBar.setVisible(False)
        listData = []
        listData.clear()
        for student in data:
            listData.append([
                student.matricule,student.level,
                self.setLabelValue(student.company, LABEL.COMPANY), 
                self.setLabelValue(student.section, LABEL.SECTION),
                student.lastname, student.firstname, student.gender
        ])
        self.view.tableView.setData(listData)
        self.view.progressBar.setValue(0)
        self.workerThread.quit()
        self.view.parent.valueCount.setText(str(len(data)))
        
    def showFilterTip(self, index):
        validate = [LABEL.COMPANY, LABEL.SECTION, LABEL.GENDER, LABEL.GRADE, LABEL.NB_DAY, LABEL.MOTIFS, LABEL.OBS]
        key = ""
        label = self.view.tableView.horizontalHeaderItem(index).text()
        if label in validate:
            data = []
            dataChecked = []
            
            if label == LABEL.COMPANY:
                key = "company"
                data = self.companyStudents
                
            elif label == LABEL.SECTION:
                data = self.sectionStudents
                key = label.lower()
                
            elif label == LABEL.GRADE:
                data = self.levelStudents
                key = "level"
                
            elif label == LABEL.GENDER:
                data = self.genderStudents
                key = "gender"
                
            elif label == LABEL.NB_DAY:
                data = self.day
                key = "day"
                
            elif label == LABEL.MOTIFS:
                data = self.motifsMove
                key = "motif"
                
            elif label == LABEL.OBS:
                data = self.obsMove
                key = "subType"
            
            posCur = QCursor().pos()
            cur_x = posCur.x()
            dataChecked = self.query.get(key) if key in self.query.keys() else []
            dataCheckedToFilter = dataChecked if len(dataChecked) > 0 else data
            filterFlyoutView = FilterFlyoutView(label, data, dataCheckedToFilter, self.view)
            
            self.popupFilter = PopupTeachingTip.make(
                target= QPoint(cur_x, 130),
                view=filterFlyoutView,
                tailPosition=TeachingTipTailPosition.TOP,
                duration=-1,
                parent=self.view
            )
            
            filterFlyoutView.yesButton.clicked.connect(lambda: self.getDataFilter(key, filterFlyoutView))
            filterFlyoutView.noButton.clicked.connect(lambda: self.popupFilter.close())
            
    def getDataFilter(self,key:str, view:FilterFlyoutView):
        self.query[key] = view.getDataFilter(self.popupFilter)
        model = self.model
        '''if self.view.parent.stackedWidget.currentIndex() == 1:
            model = self.modelMove'''
        if key == "company" or key == "section":
            self.query[key] = [val[0] for val in view.getDataFilter(self.popupFilter)]
        self.defaultData = model.fetch_all(**self.query)
        self.fetchData(self.defaultData)
        
    def setLabelValue(self, index, label):
        key = "ère" if index == 1 else "ème"
        return f'{index}{key} {label}'
        
    