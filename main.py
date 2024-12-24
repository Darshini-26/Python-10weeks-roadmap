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
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Load data if the database is empty
    load_data()

# Optionally, you can handle shutdown events if needed
@app.on_event("shutdown")
def on_shutdown():
    print("Shutting down the application...")
