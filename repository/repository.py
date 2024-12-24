from sqlalchemy.orm import Session
from models.models import Pokemon, Abilities, Stats, Types

class PokemonRepository:
    @staticmethod
    def get_all_pokemon(db: Session, offset: int, limit: int):
        return db.query(Pokemon).offset(offset).limit(limit).all()

    @staticmethod
    def get_pokemon_by_id(db: Session, pokemon_id: int):
        return db.query(Pokemon).filter(Pokemon.pokemon_id == pokemon_id).first()

    @staticmethod
    def get_pokemon_by_name(db: Session, name: str):
        return db.query(Pokemon).filter(Pokemon.name == name).first()

    @staticmethod
    def create_pokemon(db: Session, pokemon_data: Pokemon):
        db.add(pokemon_data)
        db.commit()
        db.refresh(pokemon_data)
        return pokemon_data

    @staticmethod
    def delete_pokemon(db: Session, pokemon_id: int):
        pokemon = db.query(Pokemon).filter(Pokemon.pokemon_id == pokemon_id).first()
        if pokemon:
            db.delete(pokemon)
            db.commit()
        return pokemon

    @staticmethod
    def update_pokemon(db: Session, pokemon: Pokemon):
        db.add(pokemon)
        db.commit()
        db.refresh(pokemon)
        return pokemon

    @staticmethod
    def delete_related_data(db: Session, pokemon_id: int):
        db.query(Abilities).filter(Abilities.pokemon_id == pokemon_id).delete()
        db.query(Stats).filter(Stats.pokemon_id == pokemon_id).delete()
        db.query(Types).filter(Types.pokemon_id == pokemon_id).delete()

    @staticmethod
    def add_related_data(db: Session, abilities, stats, types):
        db.add_all(abilities + stats + types)
        db.commit()
