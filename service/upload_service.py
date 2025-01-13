from typing import Type  # Add this import
from service.unit_of_work import UnitOfWork
from models import models
from schemas.schemas import PokemonResponse
from fastapi import HTTPException
import pandas as pd
import os
from repository.upload_repository import upload_to_s3

BUCKET_NAME = "pokemon-application"

def upload_all_to_s3(page:int, page_size: int,uow: UnitOfWork, model: Type[models.Base], file_name: str, columns: list = None) -> str:
    try:
        # Using the UnitOfWork context manager
        with uow:
            # Map models to repositories
            offset = (page - 1) * page_size
            repo_mapping = {
                models.Pokemon: uow.pokemons,
            }

            # Check if the model is supported
            if model not in repo_mapping:
                raise ValueError(f"Unsupported model: {model}")

            # Access the repository
            repo = repo_mapping[model]

            # Fetch data from the repository
            data = repo.get_all_pokemon(limit=page_size,offset=offset)  # Assuming get_all() method exists

            # Convert the SQLAlchemy object to a list of dictionaries using __dict__
            data_dict = [
                {key: value for key, value in record.__dict__.items() if not key.startswith('_')} 
                for record in data
            ]

            # Convert to DataFrame
            data_df = pd.DataFrame(data_dict)

            # If specific columns are provided, filter the DataFrame
            if columns:
                data_df = data_df[columns]

            # Write the data to a CSV file
            data_df.to_csv(file_name, index=False)

            # Upload the file to S3
            file_url = upload_to_s3(file_name, BUCKET_NAME)

            # Optionally delete the local file after uploading
            os.remove(file_name)

            return file_url

    except Exception as e:
        # Clean up the file if an exception occurs
        if os.path.exists(file_name):
            os.remove(file_name)
        raise e
        
def upload_by_id_to_s3(
    pokemon_id: int,
    uow: UnitOfWork,
    model: Type[models.Base],
    file_name: str,
    columns: list = None
) -> str:
    try:
        with uow:
            # Repository mapping
            repo_mapping = {models.Pokemon: uow.pokemons}
            if model not in repo_mapping:
                raise ValueError(f"Unsupported model: {model}")

            repo = repo_mapping[model]
            record = repo.get_pokemon_by_id(pokemon_id=pokemon_id)

            if not record:
                raise ValueError(f"No Pokémon found with ID: {pokemon_id}")

            # Create a dictionary of attributes explicitly
            data_dict = {
                'pokemon_id': record.pokemon_id,
                'name': record.name,
                'height': record.height,
                'weight': record.weight,
                'xp': record.xp,
                'image_url': record.image_url,
                'pokemon_url': record.pokemon_url
            }

            # Debug: Confirm the dictionary contents

            # Convert to DataFrame
            data_df = pd.DataFrame([data_dict])  # Wrap in a list for DataFrame
            print("Data dictionary:", data_df)

            if columns:
                missing_columns = [col for col in columns if col not in data_df.columns]
                if missing_columns:
                    raise ValueError(f"Columns not found in data: {missing_columns}")
                data_df = data_df[columns]

            data_df.to_csv(file_name, index=False)
            file_url = upload_to_s3(file_name, BUCKET_NAME)
            os.remove(file_name)
            return file_url

    except Exception as e:
        if os.path.exists(file_name):
            os.remove(file_name)
        raise HTTPException(status_code=500, detail=f"Failed to upload Pokémon data by ID: {str(e)}")
    
def upload_by_name_to_s3(
    name:str,
    uow: UnitOfWork,
    model: Type[models.Base],
    file_name: str,
    columns: list = None
) -> str:
    try:
        with uow:
            # Repository mapping
            repo_mapping = {models.Pokemon: uow.pokemons}
            if model not in repo_mapping:
                raise ValueError(f"Unsupported model: {model}")

            repo = repo_mapping[model]
            record = repo.get_pokemon_by_name(name=name)

            if not record:
                raise ValueError(f"No Pokémon found with ID: {name}")

            # Create a dictionary of attributes explicitly
            data_dict = {
                'pokemon_id': record.pokemon_id,
                'name': record.name,
                'height': record.height,
                'weight': record.weight,
                'xp': record.xp,
                'image_url': record.image_url,
                'pokemon_url': record.pokemon_url
            }

            # Debug: Confirm the dictionary contents

            # Convert to DataFrame
            data_df = pd.DataFrame([data_dict])  # Wrap in a list for DataFrame
            print("Data dictionary:", data_df)

            if columns:
                missing_columns = [col for col in columns if col not in data_df.columns]
                if missing_columns:
                    raise ValueError(f"Columns not found in data: {missing_columns}")
                data_df = data_df[columns]

            data_df.to_csv(file_name, index=False)
            file_url = upload_to_s3(file_name, BUCKET_NAME)
            os.remove(file_name)
            return file_url

    except Exception as e:
        if os.path.exists(file_name):
            os.remove(file_name)
        raise HTTPException(status_code=500, detail=f"Failed to upload Pokémon data by ID: {str(e)}")