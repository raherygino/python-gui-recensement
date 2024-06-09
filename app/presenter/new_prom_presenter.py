from ..view import NewPromotionDialog
from ..models import PromotionModel, Promotion
from ..common import Function

class NewPromotionPresenter:

    def __init__(self, view, model:PromotionModel, parentPresenter):
        self.view = view
        self.model = model
        self.parentPresenter = parentPresenter
        self.func = Function()
        
    def dialogNew(self, event, **kwargs):
        dialog = NewPromotionDialog(self.view)
        isUpdate = False
        promotion = None
        if len(kwargs) != 0:
            isUpdate = True
            promotion = kwargs.get("promotion")
            dialog.nameLineEdit.lineEdit.setText(promotion.name)
            dialog.rankLineEdit.spinbox.setValue(int(promotion.rank))
            dialog.logoLineEdit.lineEdit.setText(promotion.logo)
            dialog.yearLineEdit.lineEdit.setText(promotion.years)
            dialog.yesButton.setText("Mettre à jour")
        if dialog.exec():
            name = dialog.nameLineEdit.lineEdit.text()
            rank = dialog.rankLineEdit.spinbox.text()
            logo = dialog.logoLineEdit.lineEdit.text()
            years = dialog.yearLineEdit.lineEdit.text()
            nwLogo = logo
            if isUpdate:
                if promotion.logo != logo:
                    self.func.deleteFile(promotion.logo)
                    nwLogo = self.func.copyFileToFolderApp(logo, name=f"logo_{rank.replace(" ", "_")}")
                self.model.update_item(promotion.id, name=name, rank=rank, logo=nwLogo, years=years)
            else:
                if (len(logo) != 0):
                    nwLogo = self.func.copyFileToFolderApp(logo, name=f"logo_{rank.replace(" ", "_")}")
                    
                prom = Promotion(name=name, rank=rank, logo=nwLogo, years=years)
                self.model.create(prom)
            self.parentPresenter.fetchProm()