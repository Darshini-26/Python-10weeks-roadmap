from config.database import Base, engine
from models.models import Pokemon,Abilities,Stats,Types,Base
from sqlalchemy.orm import Session

def load_data():
    Base.metadata.create_all(bind=engine)  # Ensure tables exist

    with Session(bind=engine) as session:
        # Check if any Pokémon already exist
        existing_count = session.query(Pokemon).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} Pokémon. Skipping data load.")
            return

        with open("pokedex_raw_array.json", "r") as file:
            data = json.load(file)

        for pokemon_entry in data:
            print(f"Name: {pokemon_entry['name']}, Types: {pokemon_entry.get('types')}")
            try:
                # Create a Pokemon instance
                pokemon = Pokemon(
                    name=pokemon_entry["name"],
                    height=str(pokemon_entry["height"]),
                    weight=str(pokemon_entry["weight"]),
                    xp=pokemon_entry["xp"],
                    image_url=pokemon_entry["image_url"],
                    pokemon_url=pokemon_entry["pokemon_url"],
                )
                session.add(pokemon)
                session.flush()  # Generate ID

                # Add related data
                abilities = [
                    Abilities(pokemon_id=pokemon.pokemon_id, **ability)
                    for ability in pokemon_entry["abilities"]
                ]
                stats = [
                    Stats(pokemon_id=pokemon.pokemon_id, **stat)
                    for stat in pokemon_entry["stats"]
                ]
                types = [
                    Types(pokemon_id=pokemon.pokemon_id, **poke_type)
                    for poke_type in pokemon_entry["types"]
                ]
                print(f"Inserting types for Pokémon {pokemon.name}: {types}")
                session.add_all(abilities + stats + types)
            except Exception as e:
                print(f"Error processing Pokémon {pokemon_entry['name']}: {e}")

        session.commit()
        print("Data successfully loaded into the database.")

