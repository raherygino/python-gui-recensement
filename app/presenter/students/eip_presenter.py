from PyQt5.QtCore import QTimer
from .base_student_presenter import BaseStudentPresenter
from ...models import Marks
from ...common.constants import LABEL
from ...common import Function

class EipPresenter(BaseStudentPresenter):
    
    def __init__(self, parent):
        super().__init__(parent.view.eipInterface, parent)
        self.func = Function()
        self.labels = [LABEL.MATRICULE, LABEL.GRADE,LABEL.LASTNAME,LABEL.FIRSTNAME, LABEL.GENDER]
        self.mainView.subjectRefresh.connect(self.refreshSubject)
        self.table = self.view.tableView
        self.table.setSortingEnabled(True)
        self.table.itemChanged.connect(self.itemChanged)
        self.subjects = []
        self.data = []
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.fetchAll)
        
    def fetchData(self, data):
        self.view.progressBar.setVisible(True)
        self.timer.start()
    
    def refreshSubject(self, level):
        if level == "EIP":
            self.data.clear()
            self.setPromotionId(self.promotionId)
        
    def fetchAll(self):
        self.subjects = self.modelSubject.fetch_all(promotion_id=self.promotionId, level="EIP")
        data = self.model.fetchNote(self.promotionId, self.subjects, "EIP")
        for item in data:
            new_row = []
            for it in item:
                new_row.append(it if it != None else "")
            self.data.append(new_row)
        self.actionWorkerThread(data)
        self.timer.stop()
        
    def findSubjectIdByAbrv(self, abrv:str):
        subjectId = 0
        for subject in self.modelSubject.fetch_all(promotion_id=self.promotionId, level="EIP"):
            if subject.abrv == abrv:
                subjectId = subject.id
        return subjectId
            
    def findStudentIdByMatricule(self, matricule:int):
        studentId = 0
        for student in self.defaultData:
            if student.matricule == matricule:
                studentId = student.id
        return studentId
            
    def itemChanged(self, item):
        maxCol = len(self.labels)+len(self.subjects)
        if item.column() > 4 and item.column() < maxCol:
            old = self.strToFloat(self.data[item.row()][item.column()])
            new = self.strToFloat(item.text())
            if old != new:
                self.data[item.row()][item.column()] = new
                self.calculateCoef(item)
                mark = self.markFromItem(item)
                marks = self.modelMark.fetch_all(student_id=mark.student_id, subject_id=mark.subject_id)
                if len(marks) == 0:
                    if mark.value != "":
                        self.modelMark.prepareCreate(mark)
                else:
                    self.modelMark.update_item(marks[0].id, value=str(mark.value))
                self.modelMark.commit()
                self.table.resizeColumnToContents(item.column())
                self.calculateRank()
            else:
                item.setText(self.strToFloat(item.text()))
            
    def calculateCoef(self, item):
        maxCol = len(self.labels)+len(self.subjects)
        if item.column() > 4 and item.column() < maxCol:
            col = item.column()+len(self.subjects)
            pos = item.column() - len(self.labels)
            result = float(item.text() if item.text() != "" else 0) * self.subjects[pos].coef
            nItem = self.view.tableView.item(item.row(),col)
            if nItem != None:
                nItem.setText(self.strToFloat(result if item.text() != "" else item.text()))
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
                    totalItem.setText(self.strToFloat(sum(allMarks)))
                if avgItem != None:
                    avgItem.setText(self.strToFloat(avg))
            
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
                    self.table.item(item.row(), nMaxCol).setText(self.strToFloat(sum(allMarks)))
                    self.table.item(item.row(), nMaxCol+1).setText(self.strToFloat(avg))
            
    def strToFloat(self, string:str):
        value = string
        if self.func.isFloat(value):
            value = str("{:.2f}".format(float(value)))
        else:
            value = ""
        return value
        
    def markFromItem(self, item):
        value = self.strToFloat(item.text())
        item.setText(str(value))
        
        matricule = self.view.tableView.item(item.row(), 0).text()
        abrv = self.view.tableView.horizontalHeaderItem(item.column()).text()
        studentId = self.findStudentIdByMatricule(int(matricule))
        subjectId = self.findSubjectIdByAbrv(abrv)
        return Marks(promotion_id=self.promotionId, student_id=studentId, subject_id=subjectId, value=value)
            
    def setPromotionId(self, promotionId):
        self.setLabelIntoTable(promotionId, level="EIP")
        return super().setPromotionId(promotionId)
    
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
                itemAvg.setText(itemVal.zfill(len(str(len(self.data)))))
            
    def handleResult(self, data: list):
        self.view.progressBar.setVisible(False)
        listData = []
        lenSub = len(self.subjects)
        for item in data:
            nItem  = list(item)
            listData.append(nItem)
        self.view.tableView.setData(listData)
        self.calculateAVG()
        self.view.tableView.isIncrement = True
        sPos = len(self.labels) + lenSub
        self.calculateRank()
        self.view.tableView.disableEdit(sPos, self.view.tableView.columnCount())
        self.view.progressBar.setValue(0)
        self.workerThread.quit()
        self.view.parent.valueCount.setText(str(len(listData)))
        