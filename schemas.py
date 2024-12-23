from typing import List
from pydantic import BaseModel


class Ability(BaseModel):
    # pokemon_id: int
    name: str
    is_hidden: bool

    class Config:
        from_attributes = True


class Stat(BaseModel):
    name: str
    base_stat: int

    class Config:
        from_attributes = True


class Type(BaseModel):
    name: str

    class Config:
        from_attributes = True


class PokemonBase(BaseModel):
    pokemon_id: int
    name: str
    height: int
    weight: int
    xp: int
    image_url: str
    pokemon_url: str


class PokemonResponse(BaseModel):
    #pokemon_id: int
    name: str
    height: int
    weight: int
    xp: int
    image_url: str
    pokemon_url: str
    abilities: List[Ability]
    stats: List[Stat]
    types: List[Type]

    class Config:
        from_attributes = True


class PokemonOutput(PokemonBase):
    #pokemon_id: int
    abilities: List[Ability]
    stats: List[Stat]
    types: List[Type]

    class Config:
        from_attributes = True
