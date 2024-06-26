from ...view import NewStudentDialog, ShowStudentDialog
from ...models import StudentModel, Student

class ActionPresenter:
    
    def __init__(self, parent):
        self.presenter = parent
        self.view = parent.view
        self.model:StudentModel = parent.model
        
    def studentByMatricule(self, matricule) -> Student:
        return self.model.fetch_item(matricule=matricule, promotion_id=self.presenter.promotionId)
        
    def showStudent(self, matricule):
        dialog = ShowStudentDialog(self.view.parent.nParent)
        student = self.studentByMatricule(matricule)
        dialog.exec()
        
    def editStudent(self, matricule):
        dialog = NewStudentDialog(self.view.parent.nParent)
        student = self.studentByMatricule(matricule)  
        dialog.matriculeEdit.lineEdit.setText(str(student.matricule))
        dialog.lastnameEdit.lineEdit.setText(student.lastname)
        dialog.firstnameEdit.lineEdit.setText(student.firstname)
        dialog.genderEdit.combox.setCurrentIndex(1 if student.gender == 'F' else 0)
        dialog.gradeEdit.combox.setCurrentIndex(1 if student.level == 'EAP' else 0)
        dialog.yesBtn.clicked.connect(lambda: self.updateStudent(dialog))
        dialog.exec()
    
    def updateStudent(self, dialog: NewStudentDialog):
        lastname =  dialog.lastnameEdit.lineEdit.text()
        firstname = dialog.firstnameEdit.lineEdit.text()
        matricule = dialog.matriculeEdit.lineEdit.text()
        gender =    dialog.genderEdit.combox.currentText()
        grade =     dialog.gradeEdit.combox.currentText()
