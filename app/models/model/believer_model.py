from ..entity import Believer
from .base_model import Model

class BelieverModel(Model):
    def __init__(self):
        super().__init__("believers", Believer())
        
    def seed(self, count):
        for i in range(0,count):
            self.create(Believer(is_leader=1, lastname=f'Lastname {i}', firstname=f'Firstname {i}'))