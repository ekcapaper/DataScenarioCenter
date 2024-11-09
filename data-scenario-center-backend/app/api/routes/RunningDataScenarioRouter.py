from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.api.dto.CamelModel import CamelModel
from app.core.DataScenarioManager import data_scenario_manager_instance, DataScenarioNotFoundError
from app.api.dto.ResponseDSC import ResponseDSC

router = APIRouter()

class RequestCreateRunningScenario(CamelModel):
    scenario_name: str

class ResponseCreateRunningScenario(CamelModel):
    uid: str


# 시나리오 시작
@router.post("/running-scenarios/", response_model=ResponseDSC[ResponseCreateRunningScenario])
def start_scenario(request_create_running_scenario: RequestCreateRunningScenario):
    try:
        uid = data_scenario_manager_instance.run_scenario(request_create_running_scenario)
        return ResponseDSC(
            success=True,
            data=ResponseCreateRunningScenario(uid=uid),
            errors=None
        )
    except DataScenarioNotFoundError:
        raise HTTPException(status_code=404, detail="Scenario not found")


class DataScenarioExecutorDto(CamelModel):
    name: str
    description: str
    conda_environment: str
    script_path: str
    uid: str


class DataScenarioExecutorListDto(CamelModel):
    data_scenario_executor_list: list[DataScenarioExecutorDto]



