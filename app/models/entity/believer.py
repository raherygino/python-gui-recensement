    # coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Believer(Entity):
    """Environement information """
    id: int = 0
    lastname: str = None
    firstname: str = None
    address: str = None
    region: str = None
    diacon: str = None
    birthday: str = None
    birthplace: str = None
    name_father: str = None
    id_father: int = 0
    name_mother: str = None
    id_mother: int = 0
    date_of_baptism: str = None
    place_of_baptism: str = None
    date_of_recipient: str = None
    place_of_recipient: str = None
    number_recipient: str = None
    phone: str = None
    dept_work: str = None
    responsibility: str = None