from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QPoint
from qfluentwidgets import RoundMenu, Action, FluentIcon, MenuAnimationType
from .base_student_presenter import BaseStudentPresenter
from ...common.constants import *
from ...models import Student

class StudentAbsPresenter(BaseStudentPresenter):
    
    def __init__(self, parent):
        super().__init__(parent.view.absInterface, parent)
        self.__initWidget()
        self.actions()
        
    def __initWidget(self):
        self.headerLabel = [
            LABEL.MATRICULE, LABEL.GRADE, LABEL.COMPANY, LABEL.SECTION, 
            LABEL.LASTNAME,LABEL.FIRSTNAME, LABEL.GENDER, LABEL.OBS, 
            LABEL.MOTIFS, LABEL.START_DATE, LABEL.END_DATE, LABEL.NB_DAY, EMPTY]
        self.view.tableView.setHorizontalHeaderLabels(self.headerLabel)
        
    def actions(self):
        self.view.parent.nParent.refresh.connect(self.refresh)
        
    def mouseRightClick(self, event):
        headerLen = int(len(self.headerLabel)-1)
        rowSelected = int(len(self.view.tableView.selectedItems())/headerLen)
        selectedItems = self.view.tableView.selectedItems()
        '''if (len(selectedItems) != 0):
            matricule = selectedItems[0].text()
            obs = selectedItems[7].text()
            motif = selectedItems[8].text()
            start_date = selectedItems[9].text()
            end_date = selectedItems[10].text()
            day = selectedItems[11].text()
            action = MenuAction(self)
            menu = RoundMenu(parent=self.view)
            if rowSelected == 1:
                menu.addAction(Action(FluentIcon.FOLDER, 'Voir', triggered = lambda:action.show(matricule)))
                menu.addSeparator()
                menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', 
                                  triggered = lambda: action.deleteMove(matricule=matricule, 
                                                                        subType=obs, 
                                                                        motif=motif, 
                                                                        date_start = start_date, 
                                                                        date_end = end_date, 
                                                                        day = day)))
            else:
                items = []
                for index in range(rowSelected):
                    item = {
                        "promotion_id": self.promotionId,
                        "matricule": selectedItems[0+(headerLen*index)].text(),
                        "subType": selectedItems[7+(headerLen*index)].text(),
                        "motif": selectedItems[8+(headerLen*index)].text(),
                        "date_start": selectedItems[9+(headerLen*index)].text(),
                        "date_end": selectedItems[10+(headerLen*index)].text(),
                        "day": selectedItems[11+(headerLen*index)].text()
                    }
                    items.append(item)
                menu.addAction(
                    Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda : action.deleteMultipleMove(items)))
        

            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)'''
    
                
    def setPromotionId(self, promotionId):
        self.promotionId = promotionId
        self.query = {"promotion_id":promotionId}
        #self.defaultData = self.modelMove.fetch_all(**self.query)
        #self.fetchData(self.defaultData)
        
    def refresh(self, val):
        pass
        '''if "mouvement" in val:
            self.fetchData(self.modelMove.fetch_all(**self.query))'''
        
    def fetchData(self, data):
        self.intColFilter()
        self.day = list(map(str, self.fetchDataGroup(self.modelMove, key="day")))
        self.actionWorkerThread(data)
        self.workerThread.start()

    def handleResult(self, data:list):
        self.view.progressBar.setVisible(False)
        '''listData = []
        listData.clear()
        for move in data:
            student: Student = eval(move.student)
            listData.append([move.matricule, move.level,
                             self.setLabelValue(student.company,LABEL.COMPANY), 
                             self.setLabelValue(student.section,LABEL.SECTION),
                             student.lastname,student.firstname, student.gender, move.subType, 
                             move.motif, move.date_start, move.date_end, move.day])
    
        self.view.tableView.setData(listData)
        self.view.progressBar.setValue(0)
        self.workerThread.quit()
        self.view.parent.valueCount.setText(str(len(data)))'''