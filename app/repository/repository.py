from sqlalchemy.orm import Session
from app.models.models import Pokemon, Abilities, Stats, Types
from sqlalchemy.orm import joinedload

class PokemonRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_pokemon(self, offset: int=1, limit: int=25):
        return self.session.query(Pokemon).offset(offset).limit(limit).all()

    def get_pokemon_by_id(self, pokemon_id: int=1):
        return self.session.query(Pokemon).filter(Pokemon.pokemon_id == pokemon_id).first()

    def get_pokemon_by_name(self, name: str):
        return self.session.query(Pokemon).filter(Pokemon.name == name).first()

    def create_pokemon(self, pokemon_data: Pokemon):
        self.session.add(pokemon_data)
        self.session.flush()  # Ensures `pokemon_id` is generated before related data is added
        return pokemon_data

    def delete_pokemon(self, pokemon_id: int):
        pokemon = self.session.query(Pokemon).filter(Pokemon.pokemon_id == pokemon_id).first()
        if pokemon:
            self.session.delete(pokemon)
        return pokemon

    def update_pokemon(self, pokemon: Pokemon):
        self.session.add(pokemon)
        self.session.flush()
        return pokemon

    def delete_related_data(self, pokemon_id: int):
        self.session.query(Abilities).filter(Abilities.pokemon_id == pokemon_id).delete()
        self.session.query(Stats).filter(Stats.pokemon_id == pokemon_id).delete()
        self.session.query(Types).filter(Types.pokemon_id == pokemon_id).delete()

    def add_related_data(self, abilities, stats, types):
        self.session.add_all(abilities + stats + types)

    def get_all_pokemon_with_relations(self, offset: int, limit: int):
        return self.session.query(Pokemon).options(
            joinedload(Pokemon.abilities),
            joinedload(Pokemon.stats),
            joinedload(Pokemon.types)
        ).offset(offset).limit(limit).all()
    
    def get_pokemon_by_name_with_relations(self, name: str):
        return self.session.query(Pokemon).options(
            joinedload(Pokemon.abilities),  # Eager load abilities
            joinedload(Pokemon.stats),      # Eager load stats
            joinedload(Pokemon.types)       # Eager load types
        ).filter(Pokemon.name == name).first()
    
    def get_pokemon_by_id_with_relations(self, pokemon_id: int):
        return self.session.query(Pokemon).options(
            joinedload(Pokemon.abilities),
            joinedload(Pokemon.stats),
            joinedload(Pokemon.types)
        ).filter(Pokemon.pokemon_id == pokemon_id).first()

