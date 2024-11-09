import asyncio
import logging
import os
import sys
import pathlib
from typing import Optional

import aiofiles
import yaml
from watchfiles import awatch

from app.entities.DataScenario import DataScenario
from app.entities.DataScenarioExecutor import DataScenarioExecutor
from app.core.DataScenarioCenterSettings import DataScenarioCenterSettings
from loguru import logger

class DataScenarioError(Exception):
    pass

class DataScenarioNotFoundError(DataScenarioError):
    pass


class DataScenarioManager:
    __instance = None

    def __init__(self, data_scenario_center_settings: DataScenarioCenterSettings):
        self.__logger = logger.bind(class_name=self.__class__.__name__)
        self.__data_scenario_center_settings = data_scenario_center_settings

        self.__data_scenario_executors = {}


    @classmethod
    def get_instance(cls, data_scenario_center_settings: DataScenarioCenterSettings):
        if cls.__instance is None:
            cls.__instance = cls(data_scenario_center_settings)
        return cls.__instance

    # data scenario functions
    def start_data_scenario(self, name: str):
        self.get_data_scenario(name).start()

    async def stop_data_scenario(self, name: str):
        self.get_data_scenario(name).stop()

    def get_data_scenario(self, name: str) -> DataScenarioExecutor:
        return self.__data_scenario_executors[name]

    @property
    def data_scenario_executors(self):
        return self.__data_scenario_executors

    # data scenarios function
    async def refresh_data_scenario(self):
        async def load_yaml(file_path):
            async with aiofiles.open(file_path, mode='r') as file:
                contents = await file.read()
                return yaml.safe_load(contents)

        def search_paths_data_scenario_yaml_file(directory):
            yaml_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('data-scenario.yaml'):
                        yaml_files.append(os.path.join(root, file))
            return yaml_files

        # 1. stop executors
        for data_scenario_name in self.__data_scenario_executors.keys():
            await self.stop_data_scenario(data_scenario_name)

        # 2. reset
        self.__data_scenario_executors = {}

        # 3. reload
        data_scenario_yaml_paths = search_paths_data_scenario_yaml_file(self.__data_scenario_center_settings.projects_path)
        for data_scenario_path in data_scenario_yaml_paths:
            data_scenario_path = str(data_scenario_path)
            try:
                yaml_dict = await load_yaml(data_scenario_path)
                script_path = pathlib.Path(data_scenario_path)
                data_scenario_data = yaml_dict["DataScenario"]
                data_scenario = DataScenario(
                                    name=data_scenario_data["name"],
                                    description=data_scenario_data["description"],
                                    conda_environment=data_scenario_data["conda-environment"],
                                    script_path=script_path
                                )
                data_scenario_executor = DataScenarioExecutor(data_scenario)
                self.__data_scenario_executors[data_scenario.name] = data_scenario_executor
            except KeyError as ke:
                self.__logger.error(f"{data_scenario_path} is not enough values")
                self.__logger.error(ke)
