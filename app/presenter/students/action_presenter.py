from qfluentwidgets import Dialog
from ...view import NewStudentDialog, ShowStudentDialog
from ...models import StudentModel, Student
from ...common import Utils

class ActionPresenter:
    
    def __init__(self, parent):
        self.presenter = parent
        self.view = parent.view
        self.model:StudentModel = parent.model
        self.utils = Utils()
        
    def studentByMatricule(self, matricule) -> Student:
        return self.model.fetch_item(matricule=matricule, promotion_id=self.presenter.promotionId)
        
    def showStudent(self, matricule):
        dialog = ShowStudentDialog(self.view.parent.nParent)
        student = self.studentByMatricule(matricule)
        dialog.exec()
        
    def deleteStudent(self, matricule):
        dialog = Dialog('Suppimer', 'Voulez-vous le suppimer vraiment?', self.view)
        dialog.setTitleBarVisible(False)
        if dialog.exec():
            self.model.delete_by(promotion_id=self.presenter.promotionId, matricule=matricule)
            self.presenter.setPromotionId(self.presenter.promotionId)
            self.utils.infoBarSuccess("Succès", "Suppression avec réussite", self.view)
            
    def deleteMultiple(self, matricules):
        dialog = Dialog('Suppimer', 'Voulez-vous le suppimer vraiment?', self.view)
        dialog.setTitleBarVisible(False)
        if dialog.exec():
            items = [{'promotion_id':self.presenter.promotionId, 'matricule':matricule} for matricule in matricules]
            self.model.delete_mutlitple(items)
            self.presenter.setPromotionId(self.presenter.promotionId)
            self.utils.infoBarSuccess("Succès", "Suppression avec réussite", self.view)
        
    def editStudent(self, matricule):
        dialog = NewStudentDialog(self.view.parent.nParent)
        student = self.studentByMatricule(matricule)  
        dialog.titleLabel.setText(f'Modifier {student.level} {student.lastname}')
        dialog.matriculeEdit.lineEdit.setText(str(student.matricule))
        dialog.matriculeEdit.lineEdit.setEnabled(False)
        dialog.lastnameEdit.lineEdit.setText(student.lastname)
        dialog.firstnameEdit.lineEdit.setText(student.firstname)
        dialog.genderEdit.combox.setCurrentIndex(1 if student.gender == 'F' else 0)
        dialog.gradeEdit.combox.setCurrentIndex(1 if student.level == 'EAP' else 0)
        dialog.yesBtn.clicked.connect(lambda: self.updateStudent(student, dialog))
        dialog.exec()
    
    def updateStudent(self,oldStudent:Student, dialog: NewStudentDialog):
        lastname  = dialog.lastnameEdit.lineEdit.text()
        firstname = dialog.firstnameEdit.lineEdit.text()
        grade     = dialog.gradeEdit.combox.currentText()
        gender    = dialog.genderEdit.combox.currentText()
        self.model.update_item(oldStudent.id, lastname=lastname, firstname=firstname, gender=gender, level=grade)
        self.presenter.setPromotionId(self.presenter.promotionId)
        self.utils.infoBarSuccess("Succès", "Mise à jour avec réussite", self.view)
        dialog.accept()