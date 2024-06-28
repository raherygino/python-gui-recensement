from .base_tab import StudentTab

class DatabaseStudentTab(StudentTab):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tableView.setColumnNoEditable(0,8)