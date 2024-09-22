from ..entity import Diacon
from .base_model import Model

class DiaconModel(Model):
    def __init__(self):
        super().__init__("diacons", Diacon())