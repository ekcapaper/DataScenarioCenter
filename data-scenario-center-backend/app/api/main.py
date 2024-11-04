from fastapi import APIRouter

from app.api.routes import DataScenarioRouter
from app.api.routes import RunningDataScenarioRouter

api_router = APIRouter()
api_router.include_router(DataScenarioRouter.router)
api_router.include_router(RunningDataScenarioRouter.router)
