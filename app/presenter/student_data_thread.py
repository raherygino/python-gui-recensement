from PyQt5.QtCore import  QThread, pyqtSignal
from ..models import MouvementModel

class DataThread(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, data, model:MouvementModel, labels, comportement, parent=None):
        super(DataThread, self).__init__(parent)
        self.data = data
        self.model = model
        self.listStudent = []
        self.labels = labels
        self.comportement = comportement
        self.data2 = self.model.fetch_all_items()
    
    def findMove(self, col, value, move):
        isFound = move.find(f'{col}=\'{value}\'')
        if str(type(value)).find('str') != -1:
            if value.find('\'') != -1:
                isFound = move.find(f'{col}=\"{value}\"')
        return isFound != -1
    
    def countMove(self, idStudent, key, valType, mouvements):
        length = 0
        cod = []
        for move in mouvements:
            if self.findMove('idStudent', idStudent, move):
                if self.findMove(key, valType, move):
                    cod.append(eval(move))
        length = len(cod)
        return length
    
    def countTypeNsubTypeMove(self, idStudent, key, valType, valSub, mouvements):
        length = 0
        cod = []
        for move in mouvements:
            if self.findMove('idStudent', idStudent, move):
                if self.findMove(key, valType, move):
                    if self.findMove("subType", valSub, move):
                        cod.append(eval(move))
        length = len(cod)
        return length
    
    def sumMove(self, idStudent, key, valType, mouvements):
        length = 0
        cod = []
        for move in mouvements:
            if self.findMove('idStudent', idStudent, move):
                if self.findMove(key, valType, move):
                    mouvement = eval(move)
                    if mouvement.day != "":
                        length += int(mouvement.day)
        
        return length    
    
    def totalDay(self, idStudent, valType, mouvements):
        days = 0
        for move in mouvements:
            for comp in self.comportement:
                if comp.abrv == valType:
                    if move.idStudent == idStudent and move.subType == comp.name:
                        days += int(move.day) if move.day != "" else 1
        return days

    def run(self):
        mouvements = []
        # Update progress bar and emit signals
        total = len(self.data2) + len(self.data)
        for i, row in enumerate(self.data2):
            # Simulate processing delay
            self.msleep(10)
            progress = int((i + 1) / total * 100)
            self.update_progress.emit(progress)
            mouvements.append(row)
            
        labels = self.labels[5:]
        for i, student in enumerate(self.data):
            self.msleep(100) if i < 10 else self.msleep(0)
            row = [
                student.matricule, student.level, student.lastname,
                student.firstname, student.gender,
            ]
            for label in labels:
                value = self.totalDay(f'{student.id}', label, mouvements)
                row.append(value if value != 0 else "")
            self.listStudent.append(row)
            progress = int((i + 1) / total * 100)
            self.update_progress.emit(progress)
        self.finished.emit()
