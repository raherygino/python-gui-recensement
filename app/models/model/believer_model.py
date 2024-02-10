from ..entity.believer import Believer
from .base_model import Model

class BelieverModel(Model):
    def __init__(self):
        super().__init__("believers", Believer())