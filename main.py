from fastapi import FastAPI
from router.router import router  # Your router containing the API routes
from config.database import engine, Base
from utils.init_db import load_data

# Initialize the FastAPI app
app = FastAPI()

# Include the router
app.include_router(router)

# Initialize the database and load data if necessary
@app.on_event("startup")
def on_startup():
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Load data if the database is empty
        load_data()

    except Exception as e:
        # Handle startup failure silently or raise an exception
        raise e

# Optionally, you can handle shutdown events if needed
@app.on_event("shutdown")
def on_shutdown():
    pass  # Can be extended to handle resource cleanup if needed
