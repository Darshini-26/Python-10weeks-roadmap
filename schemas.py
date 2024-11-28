from typing import List
from pydantic import BaseModel


class Ability(BaseModel):
    name: str
    is_hidden: bool


class Stat(BaseModel):
    name: str
    base_stat: int


class Type(BaseModel):
    name: str


class Pokemon(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    xp: int
    image_url: str
    pokemon_url: str
    abilities: List[Ability]
    stats: List[Stat]
    types: List[Type]
