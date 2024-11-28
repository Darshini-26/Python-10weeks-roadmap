from fastapi import FastAPI, HTTPException
import json
from schemas import Pokemon
from typing import List

app = FastAPI()

pokemon_db = []


@app.on_event("startup")
def load_data():
    global pokemon_db
    try:
        with open("pokedex_raw_array.json", "r") as file:
            pokemon_db.extend(json.load(file))  # converts into a list and loads it 
        print(f"Loaded {len(pokemon_db)} Pokémon.")
    except Exception as e:
        print(f"Error loading Pokémon data: {e}")
        raise


@app.get("/fetch_pokemon_id/{id}", response_model=Pokemon)
def get_pokemon_by_id(id: int):
    for i in pokemon_db:
        if i["id"] == id:
            return i
    raise HTTPException(status_code=404, detail="Pokémon not found")


@app.get("/fetch_pokemon_name/{name}", response_model=Pokemon)
def get_pokemon_by_name(name: str):
    for i in pokemon_db:
        if i["name"].lower() == name.lower():
            return i
    raise HTTPException(status_code=404, detail="Pokémon not found")


@app.post("/create_pokemon", response_model=Pokemon)
def create_pokemon(new_pokemon: Pokemon):
    for i in pokemon_db:
        if i["id"] == new_pokemon.id:
            raise HTTPException(status_code=400, detail="Pokémon with this ID already exists")
    pokemon_db.append(new_pokemon.dict())
    return new_pokemon


@app.put("/update_pokemon/{id}", response_model=Pokemon)
def update_pokemon(id: int, updated_pokemon: Pokemon):
    """Update an existing Pokémon."""
    for pokemon in pokemon_db:
        if pokemon["id"] == id:
            pokemon["name"] = updated_pokemon.name
            pokemon["weight"] = updated_pokemon.weight
            pokemon["height"] = updated_pokemon.height
            pokemon["xp"] = updated_pokemon.xp
            pokemon["image_url"] = updated_pokemon.image_url
            pokemon["pokemon_url"] = updated_pokemon.pokemon_url
            pokemon["abilities"] = updated_pokemon.abilities
            pokemon["stats"] = updated_pokemon.stats
            pokemon["types"] = updated_pokemon.types

            pokemon.update(updated_pokemon.dict(exclude_unset=True))

            return pokemon

    raise HTTPException(status_code=404, detail="Pokémon not found")

@app.delete("/delete_pokemon/{id}")
def delete_pokemon(id: int):
    for i, pokemon in enumerate(pokemon_db):
        if pokemon["id"] == id:
            deleted_pokemon = pokemon_db.pop(i)
            return {"message": f"Pokémon with ID {id} deleted.", "deleted_pokemon": deleted_pokemon}
    raise HTTPException(status_code=404, detail="Pokémon not found")


