from ..entity import Comportement
from .base_model import Model

class ComportementModel(Model):
    def __init__(self):
        super().__init__("comportements", Comportement())
        
    def check(self, comp:Comportement, col):
        entity = { col : comp.get(col) }
        return len(self.fetch_items_by_col(comp.promotion_id, **entity))