'''API must contain the following endpoints:

1. write an endpoint which takes an ID and returns all info on the Pokemon with that Pokedex number
2. write an endpoint which takes a name and returns all info on the Pokemon with that name.
3. Write CRUD operations.

Key Points:
1. Code must be in Python, but can use any API framework. 
2. The app is only allowed to make a single call to the apl at startup to obtain the dataset and cannot make a call for that dataset each time it receives a request.
3. Any solution for this is allowed, and we can discuss other possibilities you might consider if taking more time to build this.
'''


from fastapi import FastAPI, HTTPException
import json
from schemas import Pokemon
from typing import List

app = FastAPI()

pokemon_list = []


@app.on_event("startup")
def load_data():
    global pokemon_list
    try:
        with open("pokedex_raw_array.json", "r") as file:
            pokemon_list.extend(json.load(file))  # converts into a list and loads it 
        print(f"Loaded {len(pokemon_list)} Pokémon.")
    except Exception as e:
        print(f"Error loading Pokémon data: {e}")
        raise


@app.get("/fetch_pokemon_id/{id}", response_model=Pokemon)
def get_pokemon_by_id(id: int):
    if id<=len(pokemon_list):
        return pokemon_list[id-1]
    raise HTTPException(status_code=404, detail="Pokémon not found")

@app.get("/fetch_pokemon_name/{name}", response_model=Pokemon)
def get_pokemon_by_name(name: str):
    pokemon = next((poke for poke in pokemon_list if poke["name"].lower() == name.lower()), None)
    if pokemon is not None:
        return pokemon
    raise HTTPException(status_code=404, detail="Pokémon not found")



@app.post("/create_pokemon", response_model=Pokemon)
def create_pokemon(new_pokemon: Pokemon):
    """Create a new Pokémon using any()."""
    if any(poke["id"] == new_pokemon.id for poke in pokemon_list):
        raise HTTPException(status_code=400, detail="Pokémon with this ID already exists")
    pokemon_list.append(new_pokemon.dict())
    return new_pokemon


@app.put("/update_pokemon/{id}", response_model=Pokemon)
def update_pokemon(id: int, updated_pokemon: Pokemon):
    index = next((i for i, poke in enumerate(pokemon_list) if poke["id"] == id), None)
    if index is not None:
        pokemon_list[index].update(updated_pokemon.dict(exclude_unset=True))
        return pokemon_list[index]
    raise HTTPException(status_code=404, detail="Pokémon not found")



@app.delete("/delete_pokemon/{id}")
def delete_pokemon(id: int):
    """Delete a Pokémon by ID using list comprehension."""
    index = next((i for i, poke in enumerate(pokemon_list) if poke["id"] == id), None)
    if index is not None:
        deleted_pokemon = pokemon_list.pop(index)
        return {"message": f"Pokémon with ID {id} deleted.", "deleted_pokemon": deleted_pokemon}
    raise HTTPException(status_code=404, detail="Pokémon not found")


