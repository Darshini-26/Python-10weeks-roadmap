# unit_of_work.py
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from typing import Callable
from app.repository.repository import PokemonRepository 


# Abstract Unit of Work Base
class UnitOfWorkBase(ABC):
    pokemons: PokemonRepository
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.rollback()

    @abstractmethod
    def commit(self):
        """Commit the current transaction."""
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        """Rollback the current transaction."""
        raise NotImplementedError()


# Concrete Unit of Work Implementation

class UnitOfWork(UnitOfWorkBase):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory
        self._session = None
        self.pokemons = None
       

    def __enter__(self):
        self._session = self._session_factory()  # Start a new session
        self.pokemons = PokemonRepository(self._session)
        return super().__enter__() # Returning self ensures that the repositories are accessible

    def commit(self):
        """Commit the current transaction."""
        self._session.commit()

    def rollback(self):
        """Rollback the current transaction."""
        self._session.rollback()

    def __del__(self):
        """Ensure the session is closed after usage."""
        self._session.close()
