from sqlalchemy import Integer, String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from database import Base

class Pokemon(Base):
    __tablename__ = "pokemon"

    pokemon_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    xp = Column(Integer, nullable=False)
    image_url = Column(String, nullable=False)
    pokemon_url = Column(String, nullable=False)

    # Relationships
    abilities = relationship("Abilities", back_populates="pokemon", cascade="all, delete-orphan")
    stats = relationship("Stats", back_populates="pokemon", cascade="all, delete-orphan")
    types = relationship("Types", back_populates="pokemon", cascade="all, delete-orphan")


class Abilities(Base):
    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.pokemon_id"), nullable=False)
    name = Column(String, nullable=False)
    is_hidden = Column(Boolean, nullable=False)

    # Relationship
    pokemon = relationship("Pokemon", back_populates="abilities")


class Stats(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.pokemon_id"), nullable=False)
    name = Column(String, nullable=False)
    base_stat = Column(String, nullable=False)

    # Relationship
    pokemon = relationship("Pokemon", back_populates="stats")


class Types(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.pokemon_id"), nullable=False)
    name = Column(String, nullable=False)

    # Relationship
    pokemon = relationship("Pokemon", back_populates="types")
