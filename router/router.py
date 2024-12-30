from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import session
from schemas.schemas import PokemonResponse, PokemonOutput
from service.service import PokemonService
from config.database import get_db
from service.unit_of_work import UnitOfWork

router = APIRouter(prefix="/pokemon", tags=["Pokemon"])

# Dependency to provide a Unit of Work
def get_uow(db: session = Depends(get_db)):
    return UnitOfWork(db)

# Fetch all Pokémon
@router.get("/", response_model=List[PokemonOutput])
def get_all_pokemon(page: int = 1, page_size: int = 25, uow: UnitOfWork = Depends(get_uow)):
    return PokemonService.get_all_pokemon(page, page_size, uow)

# Fetch Pokémon by ID
@router.get("/{id}", response_model=PokemonResponse)
def get_pokemon_by_id(id: int, uow: UnitOfWork = Depends(get_uow)):
    return PokemonService.get_pokemon_by_id(id, uow)

# Fetch Pokémon by name
@router.get("/name/{name}", response_model=PokemonOutput)
def get_pokemon_by_name(name: str, uow: UnitOfWork = Depends(get_uow)):
    return PokemonService.get_pokemon_by_name(name, uow)

# Create a new Pokémon
@router.post("/", response_model=PokemonOutput)
def create_pokemon(pokemon: PokemonResponse, uow: UnitOfWork = Depends(get_uow)):
    return PokemonService.create_pokemon(pokemon, uow)

# Update Pokémon by ID
@router.put("/{id}", response_model=PokemonOutput)
def update_pokemon(id: int, updated_pokemon: PokemonResponse, uow: UnitOfWork = Depends(get_uow)):
    return PokemonService.update_pokemon(id, updated_pokemon, uow)

# Delete Pokémon by ID
@router.delete("/{id}", response_model=dict)
def delete_pokemon(id: int, uow: UnitOfWork = Depends(get_uow)):
    return PokemonService.delete_pokemon(id, uow)
