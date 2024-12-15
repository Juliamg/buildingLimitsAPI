import os

from fastapi import FastAPI
from app.api import building_limits, health_check
from app.services.database import Base, engine

app = FastAPI(title="Building project")

app.include_router(building_limits.router)
app.include_router(health_check.router)

# Create database tables
Base.metadata.create_all(bind=engine) # remove
