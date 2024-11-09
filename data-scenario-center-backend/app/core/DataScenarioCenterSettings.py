from typing import Optional
from pydantic_settings import BaseSettings

class DataScenarioCenterSettings(BaseSettings):
    projects_path: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
