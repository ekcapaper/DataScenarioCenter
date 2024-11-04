from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.DataScenarioManager import data_scenario_manager_instance

router = APIRouter()


# 시나리오 목록 조회
class DataScenarioDto(BaseModel):
    name: str
    description: str
    conda_environment: str
    script_path: str


class DataScenarioListDto(BaseModel):
    data_scenario_list: list[DataScenarioDto]


def convert_data_scenario_to_data_scenario_dto(data_scenario):
    return DataScenarioDto(
        name=data_scenario.name,
        description=data_scenario.description,
        conda_environment=data_scenario.conda_environment,
        script_path=data_scenario.script_path_str,
    )


@router.get("/scenarios", response_model=DataScenarioListDto)
def get_data_scenarios():
    data_scenario_dto_list = list(
        map(convert_data_scenario_to_data_scenario_dto, data_scenario_manager_instance.get_data_scenario_list()))
    return {
        "data_scenario_list": data_scenario_dto_list
    }
