from ...view import NewStudentDialog, ShowStudentDialog

class ActionPresenter:
    
    def __init__(self, parent):
        self.presenter = parent
        self.view = parent.view
        
    def showStudent(self, matricule):
        dialog = ShowStudentDialog(self.view.parent.nParent)
        dialog.exec()
        
    def editStudent(self, matricule):
        dialog = NewStudentDialog(self.view.parent.nParent)
        dialog.exec()