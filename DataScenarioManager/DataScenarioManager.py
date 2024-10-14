import asyncio
import logging
import os
import aiofiles
import pathlib

import yaml
from watchfiles import awatch
import os

import aiofiles
import yaml
from watchfiles import awatch
from DataScenario import DataScenario
from DataScenarioExecutor import DataScenarioExecutor

class DataScenarioManager:
    def __init__(self, projects_path="./projects"):
        self.__projects_path = projects_path
        self.__data_scenario_list = []
        self.__data_scenario_executor_dict = {}
        self.__logger = logging.Logger(self.__class__.__name__)

    def reset_projects_dsm(self):
        self.__data_scenario_list = []

    async def load_projects_dsm(self):
        # inner function
        async def load_yaml(file_path):
            async with aiofiles.open(file_path, mode='r') as file:
                contents = await file.read()
                return yaml.safe_load(contents)

        def get_dsm_yaml_file_paths(directory):
            yaml_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('dsm.yaml'):
                        yaml_files.append(os.path.join(root, file))
            return yaml_files
        # task
        # 1. reset
        self.reset_projects_dsm()
        # 2. get paths
        yaml_files = get_dsm_yaml_file_paths(self.__projects_path)
        # 3. load yaml
        for yaml_file in yaml_files:
            try:
                yaml_dict = await load_yaml(yaml_file)
                script_path = pathlib.Path(yaml_dict["yaml_file"]).parent / "main.py"
                self.__data_scenario_list.append(
                    DataScenario(
                        name=yaml_dict["name"],
                        description=yaml_dict["description"],
                        conda_environment=yaml_dict["conda_environment"],
                        script_path=script_path
                    )
                )
            except KeyError as ke:
                self.__logger.error(f"{yaml_file} is not enough values")
                self.__logger.error(ke)

    def get_data_scenario_list(self):
        return self.__data_scenario_list

    def get_data_scenario_executor_dict(self):
        return self.__data_scenario_executor_dict

    def get_data_scenario_executor(self, executor_uid):
        return self.__data_scenario_executor_dict[executor_uid]

    def run_scenario(self, scenario_name):
        data_scenario_list = list(filter(lambda scenario: scenario.name == scenario_name, self.__data_scenario_list))
        if len(data_scenario_list) == 0:
            return False
        else:
            data_scenario = data_scenario_list[0]
            data_scenario_executor = DataScenarioExecutor(data_scenario)
            data_scenario_executor.run()
            self.__data_scenario_executor_dict[data_scenario_executor.uid] = data_scenario_executor
            return True

    def stop_scenario(self, uid):
        self.__data_scenario_executor_dict[uid].stop()

    def kill_scenario(self, uid):
        self.__data_scenario_executor_dict[uid].stop_force()

    async def async_loop(self):
        return asyncio.gather(self.watch_project_dsm(), self.delete_end_data_scenario_executor())

    # delete end data scenario
    async def delete_end_data_scenario_executor(self):
        while True:
            end_executor_uid_list = set()
            for uid, executor_instance in self.__data_scenario_executor_dict.items():
                if executor_instance.is_started() is True and executor_instance.is_running() is False:
                    end_executor_uid_list.add(uid)
            for end_executor_uid in end_executor_uid_list:
                del self.__data_scenario_executor_dict[end_executor_uid]
            await asyncio.sleep(5)

    async def watch_project_dsm(self):
        async for changes in awatch(self.__projects_path):
            for change in changes:
                pass

if __name__ == '__main__':
    dsm = DataScenarioManager()
    asyncio.run(dsm.load_projects_dsm())
