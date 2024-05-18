from ..models import MaterialModel
from qfluentwidgets import MessageDialog

class MenuAction:
    
    def __init__(self, presenter) -> None:
        self.presenter = presenter
        self.view = presenter.view
        self.model: MaterialModel= self.presenter.model
        
    def update(self, item):
        print(item)
        
    def confirmDelete(self, item):
        dialog = MessageDialog('Supprimer', 'Voulez vous le supprimer vraiment?', self.view.parent)
        dialog.yesButton.clicked.connect(lambda: self.delete(item))
        dialog.exec_()
        
    def delete(self, item):
        self.model.delete_item(item)
        self.presenter.refresh.emit()