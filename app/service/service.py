from typing import List
from app.models.models import Pokemon
from app.repository.repository import PokemonRepository
from fastapi import HTTPException
from .unit_of_work import UnitOfWork
from app.schemas.schemas import PokemonResponse
from app.models.models import Pokemon, Abilities, Stats, Types

class PokemonService:
    @staticmethod
    def get_all_pokemon(page: int, page_size: int, uow: UnitOfWork) -> List[Pokemon]:
        offset = (page - 1) * page_size
        with uow:
            pokemon_repo=uow.pokemons
            pokemons=pokemon_repo.get_all_pokemon(offset, page_size)
            return pokemons

    @staticmethod
    def get_pokemon_by_id(pokemon_id: int, uow: UnitOfWork) -> Pokemon:
        with uow:
            pokemon_repo= uow.pokemons
            pokemon = pokemon_repo.get_pokemon_by_id(pokemon_id)
            if not pokemon:
                raise HTTPException(status_code=404, detail="Pokemon not found")
            return pokemon

    @staticmethod
    def get_pokemon_by_name(name: str, uow: UnitOfWork) -> Pokemon:
        with uow:
            pokemon_repo= uow.pokemons
            pokemon = pokemon_repo.get_pokemon_by_name(name)
            if not pokemon:
                raise HTTPException(status_code=404, detail="Pokemon not found")
            return pokemon

    @staticmethod
    def create_pokemon(pokemon_data: PokemonResponse, uow: UnitOfWork) -> Pokemon:
        with uow:
            pokemon_repo= uow.pokemons
            pokemon = Pokemon(
                name=pokemon_data.name,
                height=pokemon_data.height,
                weight=pokemon_data.weight,
                xp=pokemon_data.xp,
                image_url=pokemon_data.image_url,
                pokemon_url=pokemon_data.pokemon_url,
            )
            pokemon_repo.create_pokemon(pokemon)
            
        
            # Add related data (abilities, stats, types)
            abilities = [Abilities(pokemon_id=pokemon.pokemon_id, **a.dict()) for a in pokemon_data.abilities]
            stats = [Stats(pokemon_id=pokemon.pokemon_id, **s.dict()) for s in pokemon_data.stats]
            types = [Types(pokemon_id=pokemon.pokemon_id, **t.dict()) for t in pokemon_data.types]
            created_pokemon=pokemon_repo.add_related_data(abilities, stats, types)

            uow.commit()
            return created_pokemon

    @staticmethod
    def update_pokemon(pokemon_id: int, updated_data: PokemonResponse, uow: UnitOfWork) -> Pokemon:
        with uow:
            pokemon_repo=uow.pokemons
            pokemon = pokemon_repo.get_pokemon_by_id(pokemon_id)
            if not pokemon:
                raise HTTPException(status_code=404, detail="Pokemon not found")

            pokemon.name = updated_data.name
            pokemon.height = updated_data.height
            pokemon.weight = updated_data.weight
            pokemon.xp = updated_data.xp
            pokemon.image_url = updated_data.image_url
            pokemon.pokemon_url = updated_data.pokemon_url

            pokemon_repo.delete_related_data(pokemon_id)
            abilities = [Abilities(pokemon_id=pokemon_id, **a.dict()) for a in updated_data.abilities]
            stats = [Stats(pokemon_id=pokemon_id, **s.dict()) for s in updated_data.stats]
            types = [Types(pokemon_id=pokemon_id, **t.dict()) for t in updated_data.types]
            pokemon_repo.add_related_data(abilities, stats, types)

            updated_pokemon = pokemon_repo.update_pokemon(pokemon)
            uow.commit()
            return updated_pokemon

    @staticmethod
    def delete_pokemon(pokemon_id: int, uow: UnitOfWork) -> dict:
        with uow:
            pokemon_repo=uow.pokemons
            pokemon = pokemon_repo.delete_pokemon(pokemon_id)
            if not pokemon:
                raise HTTPException(status_code=404, detail="Pokemon not found")
            uow.commit()
            return {"message": f"Pokemon with ID {pokemon_id} has been deleted."}