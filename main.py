from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
import json
from schemas import  Ability, Stat, Type, PokemonResponse, PokemonBase,PokemonOutput
from database import SessionLocal, engine
from models import Pokemon, Abilities, Stats, Types,Base

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load data into the database during startup
@app.on_event("startup")
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


# Fetch all Pokémon
@app.get("/fetch_pokemon/", response_model=List[PokemonOutput])
def get_all_pokemon(page: int, db: Session = Depends(get_db), page_size:int=25 ):
    return db.query(Pokemon).offset((page-1)*page_size).limit(page_size).all()
 
# Fetch Pokémon by ID
@app.get("/fetch_pokemon_id/{id}", response_model=PokemonResponse)
def get_pokemon_by_id(id: int, db: Session = Depends(get_db)):
    db_pokemon = db.query(Pokemon).filter(Pokemon.pokemon_id == id).first()
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return db_pokemon

# Fetch Pokémon by name
@app.get("/fetch_pokemon_name/{name}", response_model=PokemonOutput)
def get_pokemon_by_name(name: str, db: Session = Depends(get_db)):
    db_pokemon = db.query(Pokemon).filter(Pokemon.name == name).first()
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return db_pokemon

# Create a new Pokémon
@app.post("/create_pokemon", response_model=PokemonOutput)
def create_pokemon(pokemon: PokemonResponse, db: Session = Depends(get_db)):
    new_pokemon = Pokemon(
            name=pokemon.name,
            height=pokemon.height,
            weight=pokemon.weight,
            xp=pokemon.xp,
            image_url=str(pokemon.image_url),
            pokemon_url=str(pokemon.pokemon_url),
        )
    db.add(new_pokemon)
    db.commit()
    db.refresh(new_pokemon)
    for ability in pokemon.abilities:
        new_ability = Abilities(
            pokemon_id=new_pokemon.pokemon_id,
            name=ability.name,
            is_hidden=ability.is_hidden,
        )
        db.add(new_ability)

    for stat in pokemon.stats:
        new_stat = Stats(
            pokemon_id=new_pokemon.pokemon_id,
            name=stat.name,
            base_stat=stat.base_stat,
        )
        db.add(new_stat)

    for ptype in pokemon.types:
        new_type = Types(
            pokemon_id=new_pokemon.pokemon_id,
            name=ptype.name,
        )
        db.add(new_type)

    db.commit()
    new_pokemon = get_pokemon_by_id(new_pokemon.pokemon_id, db)
    return new_pokemon

# Update Pokémon by ID
@app.put("/update_pokemon/{id}", response_model=PokemonOutput)
def update_pokemon(id: int, updated_pokemon: PokemonResponse, db: Session = Depends(get_db)):
    # Fetch the existing Pokémon
    pokemon = db.query(Pokemon).filter(Pokemon.pokemon_id == id).first()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    pokemon.name = updated_pokemon.name
    pokemon.height = updated_pokemon.height
    pokemon.weight = updated_pokemon.weight
    pokemon.xp = updated_pokemon.xp
    pokemon.image_url = updated_pokemon.image_url
    pokemon.image_url = updated_pokemon.image_url
    pokemon.pokemon_url = updated_pokemon.pokemon_url

    db.query(Abilities).filter(Abilities.pokemon_id == id).delete()
    for ability in updated_pokemon.abilities:
        new_ability = Abilities(
            pokemon_id=id,
            name=ability.name,
            is_hidden=ability.is_hidden
        )
        db.add(new_ability)

    db.query(Stats).filter(Stats.pokemon_id == id).delete()
    for stat in updated_pokemon.stats:
        new_stat = Stats(
            pokemon_id=id,
            name=stat.name,
            base_stat=stat.base_stat
        )
        db.add(new_stat)

    db.query(Types).filter(Types.pokemon_id == id).delete()
    for ptype in updated_pokemon.types:
        new_type = Types(
            pokemon_id=id,
            name=ptype.name,
        )
        db.add(new_type)

    db.commit()
    updated_pokemon = get_pokemon_by_id(id, db)
    return updated_pokemon



# Delete Pokémon by ID
@app.delete("/delete_pokemon/{id}", response_model=dict)
def delete_pokemon(id: int, db: Session = Depends(get_db)):
    db_pokemon = db.query(Pokemon).filter(Pokemon.pokemon_id == id).first()
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    db.delete(db_pokemon)
    db.commit()
    return {"message": f"Pokemon with ID {id} deleted successfully."}
