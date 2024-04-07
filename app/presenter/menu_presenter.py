from ..models import Believer, BelieverModel
from ..view import ShowBelieverDialog
from qfluentwidgets import MessageDialog

class MenuAction:
    
    def __init__(self, presenter) -> None:
        self.presenter = presenter
        self.view = presenter.view
        self.model: BelieverModel= self.presenter.model
        
    def show(self, itemId):
        believer: Believer = self.model.fetch_item_by_id(itemId)
        row1 = [
            ["Anarana", believer.lastname],
            ["Fanampiny", believer.firstname],
            ["Adiresy", believer.address],
            ["Faritra", believer.region],
            ["Diakonina miandraikitra", believer.diacon]
            ]
        
        row2 = [
            ["Daty sy toerana nahaterahana", f'{believer.birthday} {believer.birthplace}'],
            ["Anaran'i Reny", believer.name_mother],
            ["Anaran'i Ray", believer.name_father],
            ["Anaran'i Reny", believer.name_mother],
            ["Daty ny batisa", believer.date_of_baptism],
            ]
        
        row3 = [
            ["Toerana ny batisa", believer.place_of_baptism],
            ["Daty nahampandray", believer.date_of_recipient],
            ["Toerana nahampandray", believer.place_of_recipient],
            ["Laharana ny mpandray", believer.number_recipient],
            ["Laharan'ny finday", believer.phone],
            ]
        
        row4 = [
            ["Sampana na/sy sampan'asa", believer.dept_work],
                ["Andraikitra", believer.responsibility],
            ]
            
        allRows =  [row1, row2, row3, row4]
        dialog = ShowBelieverDialog(self.view)
        dialog.table.setHorizontalHeaderLabels(self.presenter.labelsFamily)
            
        for i, row in enumerate(allRows):
            for j, column in enumerate(row):
                dialog.addLabelValue(column[0], column[1], i,j)
                    
        data = self.model.fetch_all(id_conjoint=itemId)
        for value in self.model.fetch_all(id_father=itemId):
            data.append(value)
                
        self.presenter.setData(dialog.table, data)
        dialog.exec()
        
    def update(self, item):
        print(item)
        
    def confirmDelete(self, item):
        dialog = MessageDialog('Supprimer', 'Voulez vous le supprimer vraiment?', self.view.nParent)
        dialog.yesButton.clicked.connect(lambda: self.delete(item))
        dialog.exec_()
        
    def delete(self, item):
        self.model.delete_item(item)
        self.presenter.fetchData(self.model.fetch_all(**self.presenter.query))
        #self.presenter.refresh.emit()