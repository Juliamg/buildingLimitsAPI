from fastapi import FastAPI
from app.api import building_limits, health_check

app = FastAPI(title="Building project")

app.include_router(building_limits.router)
app.include_router(health_check.router)
