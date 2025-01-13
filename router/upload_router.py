from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from service.unit_of_work import UnitOfWork
from service.upload_service import upload_all_to_s3, upload_by_id_to_s3, upload_by_name_to_s3
from models import models
from config.database import SessionLocal

router = APIRouter(tags=["Upload"])

# Dependency to provide a Unit of Work
def get_uow() -> UnitOfWork:
    return UnitOfWork(SessionLocal)

@router.get("/upload/all")
def upload_all_pokemon_to_s3(page:int= Query(1,description="page" ), page_size: int= Query(25,description="page size"),uow: UnitOfWork = Depends(get_uow)):
    """
    Uploads all Pokémon data to S3 in CSV format.
    """
    try:
        file_url = upload_all_to_s3(page=page, page_size=page_size,uow=uow,model= models.Pokemon,file_name= "all_pokemon.csv")
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload Pokémon data: {str(e)}")

@router.get("/upload/{pokemon_id}")
def upload_pokemon_by_id(pokemon_id: int, uow: UnitOfWork = Depends(get_uow)):
    """
    Uploads Pokémon data for a specific Pokémon ID to S3.
    """
    try:
        # Filter Pokémon by ID in the upload logic
        file_name = f"pokemon_{pokemon_id}.csv"
        file_url = upload_by_id_to_s3(pokemon_id,uow, models.Pokemon, file_name, columns=["pokemon_id", "name", "height", "weight", "xp", "image_url", "pokemon_url"])
        return JSONResponse(content={"message": f"File uploaded for Pokémon ID {pokemon_id}", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload Pokémon data by ID: {str(e)}")

@router.get("/upload/name/{name}")
def upload_pokemon_by_name(name: str, uow: UnitOfWork = Depends(get_uow)):
    """
    Uploads Pokémon data filtered by name to S3.
    """
    try:
        # Add filtering by name logic
        file_name = f"pokemon_{name}.csv"
        file_url = upload_by_name_to_s3(name,uow, models.Pokemon, file_name, columns=["pokemon_id", "name", "height", "weight", "xp", "image_url", "pokemon_url"])
        return JSONResponse(content={"message": f"File uploaded for Pokémon name '{name}'", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload Pokémon data by name: {str(e)}")
