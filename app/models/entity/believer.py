    # coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Believer(Entity):
    """Environement information """
    id: int = None
    lastname: str = None
    firstname: str = None
    age: str = None
    icon: str = None