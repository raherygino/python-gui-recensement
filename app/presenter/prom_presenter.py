from qfluentwidgets import FluentIcon, RoundMenu, Action, MenuAnimationType, Dialog
from .new_prom_presenter import NewPromotionPresenter
from ..models import PromotionModel
from ..components.link_card2 import LinkCard
from ..common.functions import Function

class PromotionPresenter:

    def __init__(self, view, model: PromotionModel, mainWindow):
        self.view = view
        self.model = model
        self.mainView = mainWindow
        self.func = Function()
        self.nPromPresenter = NewPromotionPresenter(view, model, self)
        self.fetchProm()
        self.currentPromotion = 0
        
    def deleteBannerWidget(self):
        layout = self.view.flowLayout
        layout.takeAllWidgets()
        
    def fetchProm(self):
        self.deleteBannerWidget()
        self.btnAdd = LinkCard(FluentIcon.ADD, 'Ajouter', 'Ajouter une autre promotion', self.view)
        self.btnAdd.mouseReleaseEvent = lambda event: self.nPromPresenter.dialogNew(event)
        self.mainView.currentPromotion.connect(self.setCurrentPromotion)
        promotions = self.model.fetch_all_items(order="id DESC")
        self.view.flowLayout.addWidget(self.btnAdd)
        for promotion in promotions:
            logo = FluentIcon.PEOPLE
            if promotion.logo != "":
                logo = promotion.logo
            card = LinkCard(
                logo, 
                promotion.rank, 
                promotion.name, 
                self.view)
            card.contextMenuEvent = lambda event, promotion=promotion: self.menuCard(event, promotion)
            card.mouseDoubleClickEvent = lambda event, promotion=promotion: self.showPromotion(event, promotion)            
            self.view.flowLayout.addWidget(card)
            
    def showPromotion(self, event, promotion):
        studentsInterface = self.mainView.studentsInterface
        if self.currentPromotion != promotion.id:
            self.mainView.currentPromotion.emit(promotion.id)
        self.mainView.switchTo(studentsInterface)
        self.mainView.fluentTitleBar.subtitleLabel.setText(f'| {promotion.name if promotion.name != "" else promotion.rank}')
        
    def setCurrentPromotion(self, id:int):
        self.currentPromotion = id
        
    def menuCard(self, event, promotion):
        menu = RoundMenu(self.view)
        menu.addAction(Action(FluentIcon.FOLDER, 'Voir', triggered=lambda event: self.showPromotion(event, promotion)))
        menu.addAction(
            Action(
                FluentIcon.EDIT, 
                'Modifier', 
                triggered=lambda event : self.nPromPresenter.dialogNew(event, promotion=promotion)
                )
            )
        menu.addSeparator()
        menu.addAction(
            Action(
                FluentIcon.DELETE, 
                'Supprimer', 
                triggered=lambda: self.deletePromotion(promotion)
                )
            )
        menu.exec(event.globalPos(), aniType=MenuAnimationType.DROP_DOWN)
        
    def deletePromotion(self, promotion):
        title = 'Vous êtes sûr de vouloir supprimer?'
        content = f'Quand vous avez supprimés {promotion.rank}, toutes les données avec cette promotion seront perdues'
        w = Dialog(title, content, self.view)
        w.setTitleBarVisible(False)
        if w.exec():
            self.model.delete_item(promotion.id)
            if promotion.logo != "":
                self.func.deleteFile(promotion.logo)
            if promotion.id == self.currentPromotion:
                self.mainView.currentPromotion.emit(0)
            self.fetchProm()
            self.mainView.fluentTitleBar.subtitleLabel.setText("")