from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.api.dto.CamelModel import CamelModel
from app.api.dto.ResponseDSC import ResponseDSC
from app.core.DataScenarioManager import DataScenarioManager
from app.core.DataScenarioCenterSettings import DataScenarioCenterSettings

router = APIRouter()

def get_data_scenario_manager(data_scenario_center_settings: DataScenarioCenterSettings = Depends(DataScenarioCenterSettings)) -> DataScenarioManager:
    return DataScenarioManager(data_scenario_center_settings)


# 시나리오 목록 조회
class DataScenarioDto(CamelModel):
    name: str
    description: str
    conda_environment: str
    script_path: str


class DataScenarioListDto(CamelModel):
    data_scenario_list: list[DataScenarioDto]



@router.get("/scenarios", response_model=ResponseDSC[DataScenarioListDto])
def get_data_scenarios(
    data_scenario_manager: DataScenarioManager = Depends(get_data_scenario_manager),
):
    data_scenario_dto_list = list(map(
        lambda data_scenario:DataScenarioDto(
            name=data_scenario.name,
            description=data_scenario.description,
            conda_environment=data_scenario.conda_environment,
            script_path=data_scenario.script_path_str
        ), data_scenario_manager.data_scenarios)
    )
    return {
        "success": True,
        "data": {
            "data_scenario_list": data_scenario_dto_list
        },
        "error": None
    }
