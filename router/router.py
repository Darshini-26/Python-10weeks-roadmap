from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from schemas.schemas import PokemonResponse, PokemonOutput
from service.service import PokemonService
from config.database import get_db

router = APIRouter(prefix="/pokemon", tags=["Pokemon"])

# Fetch all Pokémon
@router.get("/", response_model=List[PokemonOutput])
def get_all_pokemon(page: int = 1, page_size: int = 25, db: Session = Depends(get_db)):
    return PokemonService.get_all_pokemon(page, page_size, db)

# Fetch Pokémon by ID
@router.get("/{id}", response_model=PokemonResponse)
def get_pokemon_by_id(id: int, db: Session = Depends(get_db)):
    return PokemonService.get_pokemon_by_id(id, db)

# Fetch Pokémon by name
@router.get("/name/{name}", response_model=PokemonOutput)
def get_pokemon_by_name(name: str, db: Session = Depends(get_db)):
    return PokemonService.get_pokemon_by_name(name, db)

# Create a new Pokémon
@router.post("/", response_model=PokemonOutput)
def create_pokemon(pokemon: PokemonResponse, db: Session = Depends(get_db)):
    return PokemonService.create_pokemon(pokemon, db)

# Update Pokémon by ID
@router.put("/{id}", response_model=PokemonOutput)
def update_pokemon(id: int, updated_pokemon: PokemonResponse, db: Session = Depends(get_db)):
    return PokemonService.update_pokemon(id, updated_pokemon, db)

# Delete Pokémon by ID
@router.delete("/{id}", response_model=dict)
def delete_pokemon(id: int, db: Session = Depends(get_db)):
    return PokemonService.delete_pokemon(id, db)
