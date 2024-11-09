from fastapi import APIRouter

from app.api.routes import DataScenarioRouter

api_router = APIRouter()
api_router.include_router(DataScenarioRouter.router)
