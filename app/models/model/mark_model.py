from ..entity import Marks
from .base_model import Model

class MarkModel(Model):
    def __init__(self):
        super().__init__("marks", Marks())