from PyQt5.QtCore import QTimer
from .base_student_presenter import BaseStudentPresenter
from ...models import Marks
from ...common.constants import LABEL
from ...common import Function

class BaseGradesPresenter(BaseStudentPresenter):
    
    def __init__(self, view, parent):
        super().__init__(view, parent)
        self.labels = [LABEL.MATRICULE, LABEL.GRADE,LABEL.LASTNAME,LABEL.FIRSTNAME, LABEL.GENDER]
        self.data = []
        self.func = Function()
        self.mainView.subjectRefresh.connect(self.refreshSubject)
        self.__init_table()
        
    def __init_table(self):
        self.table = self.view.tableView
        self.table.setSortingEnabled(True)
        self.table.itemChanged.connect(self.itemChanged)
            
    def setPromotionId(self, promotionId):
        self.setLabelIntoTable(promotionId, level=self.getLevel())
        return super().setPromotionId(promotionId)
        
    def fetchData(self, data):
        self.view.progressBar.setVisible(True)
        nData = self.model.fetchNote(self.promotionId, self.subjects, self.getLevel())
        for item in nData:
            new_row = []
            for it in item:
                new_row.append(it if it != None else "")
            self.data.append(new_row)
        self.actionWorkerThread(nData)
    
    def refreshSubject(self, level):
        self.data.clear()
        self.setPromotionId(self.promotionId)
        
    def itemChanged(self, item):
        maxCol = len(self.labels)+len(self.subjects)
        col = item.column()
        row = item.row()
        if col > 4 and col < maxCol:
            old = self.func.strToFloat(self.data[row][col])
            new = self.func.strToFloat(item.text())
            if old != new:
                self.data[row][col] = new
                self.calculateCoef(item)
                mark = self.markFromItem(item)
                marks = self.modelMark.fetch_all(student_id=mark.student_id, subject_id=mark.subject_id)
                if len(marks) == 0:
                    if mark.value != "":
                        self.modelMark.prepareCreate(mark)
                else:
                    self.modelMark.update_item(marks[0].id, value=str(mark.value))
                self.modelMark.commit()
                self.table.resizeColumnToContents(col)
                self.calculateRank()
            else:
                item.setText(self.func.strToFloat(item.text()))
            
    def calculateCoef(self, item):
        maxCol = len(self.labels)+len(self.subjects)
        if item.column() > 4 and item.column() < maxCol:
            col = item.column()+len(self.subjects)
            pos = item.column() - len(self.labels)
            result = float(item.text() if item.text() != "" else 0) * self.subjects[pos].coef
            nItem = self.view.tableView.item(item.row(),col)
            if nItem != None:
                nItem.setText(self.func.strToFloat(result if item.text() != "" else item.text()))
            self.calculateItemAVG(item)
        
    def calculateAVG(self):
        maxCol = len(self.labels)+len(self.subjects)
        nMaxCol = maxCol + len(self.subjects)
        for i, value in enumerate(self.data):
            allMarks = []
            for j in range(maxCol, nMaxCol):
                nValue = self.data[i][j]
                allMarks.append(0 if nValue == "" else float(nValue))
            totalMarks = sum(allMarks)
            totalCoef = sum([int(sub.coef) for sub in self.subjects])
            avg = totalMarks/totalCoef if totalCoef > 0 else 0
            if totalMarks != 0:
                totalItem = self.table.item(i, nMaxCol)
                avgItem = self.table.item(i, nMaxCol+1)
                if totalItem != None:
                    totalItem.setText(self.func.strToFloat(sum(allMarks)))
                if avgItem != None:
                    avgItem.setText(self.func.strToFloat(avg))
            
    def calculateItemAVG(self, item):
        maxCol = len(self.labels)+len(self.subjects)
        if item.column() > 4 and item.column() < maxCol:
            allMarks = []
            nMaxCol = maxCol + len(self.subjects)
            for i in range(maxCol, nMaxCol):
                nItem = self.table.item(item.row(), i)
                if nItem != None:
                    itemValue = nItem.text()
                    allMarks.append(0 if itemValue == "" else float(itemValue))
                    totalMarks = sum(allMarks)
                    totalCoef = sum([int(sub.coef) for sub in self.subjects])
                    avg = totalMarks/totalCoef if totalCoef > 0 else 0
                    self.table.item(item.row(), nMaxCol).setText(self.func.strToFloat(sum(allMarks)))
                    self.table.item(item.row(), nMaxCol+1).setText(self.func.strToFloat(avg))
    
    def calculateRank(self):
        lenSub = len(self.subjects)
        sPos = len(self.labels) + lenSub
        posAvg = sPos+lenSub+1
        avgs = []
        for avg in self.table.getData():
            avgs.append(float(avg[posAvg] if avg[posAvg] != '' else 0))
        sorted_list = sorted(avgs, reverse=True)
        for i, nAvg in enumerate(avgs):
            itemAvg = self.table.item(i, posAvg + 1)
            if itemAvg != None:
                itemVal = str(sorted_list.index(nAvg) + 1)
                #itemAvg.setText(itemVal.zfill(len(str(len(self.data)))))
        
    def markFromItem(self, item):
        value = self.func.strToFloat(item.text())
        matricule = self.view.tableView.item(item.row(), 0).text()
        abrv = self.view.tableView.horizontalHeaderItem(item.column()).text()
        studentId = self.findStudentIdByMatricule(int(matricule))
        subjectId = self.findSubjectIdByAbrv(abrv)
        item.setText(str(value))
        return Marks(promotion_id=self.promotionId, student_id=studentId, subject_id=subjectId, value=value)
            
    def handleResult(self, data: list):
        self.view.progressBar.setVisible(False)
        lenSub = len(self.subjects)
        listData = [list(item) for item in data]
        self.view.tableView.setData(listData)
        self.calculateAVG()
        self.view.tableView.isIncrement = True
        sPos = len(self.labels) + lenSub
        self.calculateRank()
        self.view.tableView.disableEdit(sPos, self.view.tableView.columnCount())
        self.view.progressBar.setValue(0)
        self.workerThread.quit()
        self.view.parent.valueCount.setText(str(len(listData)))
        