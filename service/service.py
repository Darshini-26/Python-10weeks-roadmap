from sqlalchemy.orm import Session
from typing import List
from models.models import Pokemon, Abilities, Stats, Types
from schemas.schemas import PokemonResponse
from repository.repository import PokemonRepository
from fastapi import HTTPException

class PokemonService:
    @staticmethod
    def get_all_pokemon(page: int, page_size: int, db: Session) -> List[Pokemon]:
        offset = (page - 1) * page_size
        return PokemonRepository.get_all_pokemon(db, offset, page_size)

    @staticmethod
    def get_pokemon_by_id(pokemon_id: int, db: Session) -> Pokemon:
        pokemon = PokemonRepository.get_pokemon_by_id(db, pokemon_id)
        if not pokemon:
            raise HTTPException(status_code=404, detail="Pokemon not found")
        return pokemon

    @staticmethod
    def get_pokemon_by_name(name: str, db: Session) -> Pokemon:
        pokemon = PokemonRepository.get_pokemon_by_name(db, name)
        if not pokemon:
            raise HTTPException(status_code=404, detail="Pokemon not found")
        return pokemon

    @staticmethod
    def create_pokemon(pokemon_data: PokemonResponse, db: Session) -> Pokemon:
        # Create the base Pokémon record
        pokemon = Pokemon(
            name=pokemon_data.name,
            height=pokemon_data.height,
            weight=pokemon_data.weight,
            xp=pokemon_data.xp,
            image_url=pokemon_data.image_url,
            pokemon_url=pokemon_data.pokemon_url,
        )
        PokemonRepository.create_pokemon(db, pokemon)

        # Add related data (abilities, stats, types)
        abilities = [Abilities(pokemon_id=pokemon.pokemon_id, **a.dict()) for a in pokemon_data.abilities]
        stats = [Stats(pokemon_id=pokemon.pokemon_id, **s.dict()) for s in pokemon_data.stats]
        types = [Types(pokemon_id=pokemon.pokemon_id, **t.dict()) for t in pokemon_data.types]
        PokemonRepository.add_related_data(db, abilities, stats, types)

        return pokemon

    @staticmethod
    def update_pokemon(pokemon_id: int, updated_data: PokemonResponse, db: Session) -> Pokemon:
        # Fetch the Pokémon to update
        pokemon = PokemonRepository.get_pokemon_by_id(db, pokemon_id)
        if not pokemon:
            raise HTTPException(status_code=404, detail="Pokemon not found")

        # Update base fields
        pokemon.name = updated_data.name
        pokemon.height = updated_data.height
        pokemon.weight = updated_data.weight
        pokemon.xp = updated_data.xp
        pokemon.image_url = updated_data.image_url
        pokemon.pokemon_url = updated_data.pokemon_url

        # Update related data
        PokemonRepository.delete_related_data(db, pokemon_id)
        abilities = [Abilities(pokemon_id=pokemon_id, **a.dict()) for a in updated_data.abilities]
        stats = [Stats(pokemon_id=pokemon_id, **s.dict()) for s in updated_data.stats]
        types = [Types(pokemon_id=pokemon_id, **t.dict()) for t in updated_data.types]
        PokemonRepository.add_related_data(db, abilities, stats, types)

        return PokemonRepository.update_pokemon(db, pokemon)

    @staticmethod
    def delete_pokemon(pokemon_id: int, db: Session) -> dict:
        pokemon = PokemonRepository.delete_pokemon(db, pokemon_id)
        if not pokemon:
            raise HTTPException(status_code=404, detail="Pokemon not found")
        return {"message": f"Pokemon with ID {pokemon_id} deleted successfully."}
