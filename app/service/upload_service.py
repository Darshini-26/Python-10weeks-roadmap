from typing import Type  # Add this import
from app.service.unit_of_work import UnitOfWork
from app.models import models
from app.schemas.schemas import PokemonResponse
from fastapi import HTTPException
import pandas as pd
import os
from app.repository.upload_repository import upload_to_s3
from sqlalchemy.orm import joinedload

BUCKET_NAME = "pokemon-application"

def upload_all_to_s3(
    page: int,
    page_size: int,
    uow: UnitOfWork,
    model: Type[models.Base],
    file_name: str,
    columns: list = None
) -> str:
    try:
        # Using the UnitOfWork context manager
        with uow:
            offset = (page - 1) * page_size
            repo_mapping = {models.Pokemon: uow.pokemons}

            # Check if the model is supported
            if model not in repo_mapping:
                raise ValueError(f"Unsupported model: {model}")

            # Access the repository
            repo = repo_mapping[model]

            # Fetch data from the repository (including relations)
            pokemons = repo.get_all_pokemon_with_relations(offset=offset, limit=page_size)

            # Prepare the data
            data_dicts = []
            for pokemon in pokemons:
                data_dict = {
                    'pokemon_id': pokemon.pokemon_id,
                    'name': pokemon.name,
                    'height': pokemon.height,
                    'weight': pokemon.weight,
                    'xp': pokemon.xp,
                    'image_url': pokemon.image_url,
                    'pokemon_url': pokemon.pokemon_url,
                    'abilities': ', '.join([ability.name for ability in pokemon.abilities]),
                    'stats': '; '.join([f"{stat.name}: {stat.base_stat}" for stat in pokemon.stats]),
                    'types': ', '.join([type.name for type in pokemon.types]),
                }
                data_dicts.append(data_dict)

            # Convert to DataFrame
            data_df = pd.DataFrame(data_dicts)

            # Filter columns if specified
            if columns:
                missing_columns = [col for col in columns if col not in data_df.columns]
                if missing_columns:
                    raise ValueError(f"Columns not found in data: {missing_columns}")
                data_df = data_df[columns]

            # Write to a CSV file
            data_df.to_csv(file_name, index=False)

            # Upload the CSV to S3
            BUCKET_NAME = "pokemon-application"  # Replace with your bucket name
            file_url = upload_to_s3(file_name, BUCKET_NAME)

            # Clean up the local file
            os.remove(file_name)

            return file_url

    except Exception as e:
        # Clean up the file if an exception occurs
        if os.path.exists(file_name):
            os.remove(file_name)
        raise HTTPException(status_code=500, detail=f"Failed to upload Pokémon data: {str(e)}")


        
def upload_by_id_to_s3(
    pokemon_id: int,
    uow: UnitOfWork,
    model: Type[models.Base],
    file_name: str,
    columns: list = None
) -> str:
    try:
        # Using the UnitOfWork context manager
        with uow:
            # Check if the model is supported
            repo_mapping = {models.Pokemon: uow.pokemons}
            if model not in repo_mapping:
                raise ValueError(f"Unsupported model: {model}")

            # Access the repository
            repo = repo_mapping[model]

            # Fetch the data for a single Pokémon by ID (including relations)
            pokemon = repo.get_pokemon_by_id_with_relations(pokemon_id)

            # If the Pokémon doesn't exist, raise an error
            if not pokemon:
                raise ValueError(f"Pokemon with ID {pokemon_id} not found.")

            # Prepare the data
            data_dict = {
                'pokemon_id': pokemon.pokemon_id,
                'name': pokemon.name,
                'height': pokemon.height,
                'weight': pokemon.weight,
                'xp': pokemon.xp,
                'image_url': pokemon.image_url,
                'pokemon_url': pokemon.pokemon_url,
                'abilities': ', '.join([ability.name for ability in pokemon.abilities]),
                'stats': '; '.join([f"{stat.name}: {stat.base_stat}" for stat in pokemon.stats]),
                'types': ', '.join([type.name for type in pokemon.types]),
            }

            # Convert to DataFrame (just a single row)
            data_df = pd.DataFrame([data_dict])

            # Filter columns if specified
            if columns:
                missing_columns = [col for col in columns if col not in data_df.columns]
                if missing_columns:
                    raise ValueError(f"Columns not found in data: {missing_columns}")
                data_df = data_df[columns]

            # Write to a CSV file
            data_df.to_csv(file_name, index=False)

            # Upload the CSV to S3
            BUCKET_NAME = "pokemon-application"  # Replace with your bucket name
            file_url = upload_to_s3(file_name, BUCKET_NAME)

            # Clean up the local file
            os.remove(file_name)

            return file_url

    except Exception as e:
        # Clean up the file if an exception occurs
        if os.path.exists(file_name):
            os.remove(file_name)
        raise HTTPException(status_code=500, detail=f"Failed to upload Pokémon data by ID: {str(e)}")


def upload_by_name_to_s3(
    name: str,
    uow: UnitOfWork,
    model: Type[models.Base],
    file_name: str,
    columns: list = None
) -> str:
    try:
        with uow:
            repo_mapping = {models.Pokemon: uow.pokemons}
            if model not in repo_mapping:
                raise ValueError(f"Unsupported model: {model}")

            repo = repo_mapping[model]
            record = repo.get_pokemon_by_name_with_relations(name=name)

            if not record:
                raise ValueError(f"No Pokémon found with name: {name}")

            # Debugging: Check if relationships are loaded
            print(f"Fetched Pokémon: {record.name}, Abilities: {record.abilities}, Stats: {record.stats}, Types: {record.types}")

            abilities_str = ', '.join([ability.name for ability in record.abilities]) if record.abilities else ''
            stats_str = '; '.join([f"{stat.name}: {stat.base_stat}" for stat in record.stats]) if record.stats else ''
            types_str = ', '.join([type.name for type in record.types]) if record.types else ''

            # Debug: Check the formatted strings for relationships
            print("Abilities (formatted):", abilities_str)
            print("Stats (formatted):", stats_str)
            print("Types (formatted):", types_str)

            data_dict = {
                'pokemon_id': record.pokemon_id,
                'name': record.name,
                'height': record.height,
                'weight': record.weight,
                'xp': record.xp,
                'image_url': record.image_url,
                'pokemon_url': record.pokemon_url,
                'abilities': abilities_str,
                'stats': stats_str,
                'types': types_str,
            }

            # Debug: Check the data dictionary
            print("Data dictionary for CSV:", data_dict)

            data_dicts = [data_dict]  # Wrap single dict in a list

            # Convert to DataFrame
            data_df = pd.DataFrame(data_dicts)

            # Debug: Check the DataFrame before writing to CSV
            print("DataFrame before writing to CSV:", data_df.head())

            if columns:
                missing_columns = [col for col in columns if col not in data_df.columns]
                if missing_columns:
                    raise ValueError(f"Columns not found in data: {missing_columns}")
                data_df = data_df[columns]

            # Write to CSV
            print("Writing data to CSV...")
            data_df.to_csv(file_name, index=False)

            # Upload the CSV to S3
            BUCKET_NAME = "pokemon-application"  # Replace with your bucket name
            file_url = upload_to_s3(file_name, BUCKET_NAME)

            # Clean up the local file
            os.remove(file_name)

            return file_url

    except Exception as e:
        if os.path.exists(file_name):
            os.remove(file_name)
        raise HTTPException(status_code=500, detail=f"Failed to upload Pokémon data by name: {str(e)}")
