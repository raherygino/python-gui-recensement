from .base_student_presenter import BaseStudentPresenter
from ...models import Marks
from ...common.constants import LABEL
from ...common import Function
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QTimer

class EipPresenter(BaseStudentPresenter):
    
    def __init__(self, parent):
        super().__init__(parent.view.eipInterface, parent) 
        self.func = Function()
        self.labels = [LABEL.MATRICULE, LABEL.GRADE,LABEL.LASTNAME,LABEL.FIRSTNAME, LABEL.GENDER]
        self.mainView.subjectRefresh.connect(lambda level: self.setLabelIntoTable(self.promotionId, level))
        self.view.tableView.itemChanged.connect(self.itemChanged)
        self.subjects = []
        self.data = []
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.fetchAll)
        
    def fetchData(self, data):
        self.view.progressBar.setVisible(True)
        self.timer.start()
        
    def fetchAll(self):
        self.subjects = self.modelSubject.fetch_all(promotion_id=self.promotionId, level="EIP")
        data = self.model.fetchNote(self.promotionId, self.subjects)
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
        if item.column() > 4 and item.text() != "":
            old = self.strToFloat(self.data[item.row()][item.column()])
            new = self.strToFloat(item.text())
            if old != new:
                mark = self.markFromItem(item)
                marks = self.modelMark.fetch_all(student_id=mark.student_id, subject_id=mark.subject_id)
                if len(marks) == 0:
                    if mark.value != "":
                        self.modelMark.prepareCreate(mark)
                else:
                    self.modelMark.update_item(marks[0].id, value=str(mark.value))
                self.modelMark.commit()
            else:
                item.setText(self.strToFloat(item.text()))
                
            
    def strToFloat(self, string:str):
        value = string
        if self.func.isFloat(value):
            value = float(value)
            value = str("{:.2f}".format(value))
            vls = value.split('.')
            value = vls[0] if vls[1] == "00" else value
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
    
    def handleResult(self, data: list):
        self.view.progressBar.setVisible(False)
        listData = []
        lenSub = len(self.subjects)
        for item in data:
            nItem  = list(item)
            listData.append(nItem)
        self.view.tableView.setData(listData)
        self.view.tableView.isIncrement = True
        sPos = len(self.labels) + lenSub
        
        self.view.tableView.disableEdit(sPos, self.view.tableView.columnCount())
        self.view.progressBar.setValue(0)
        self.workerThread.quit()
        self.view.parent.valueCount.setText(str(len(listData)))
        