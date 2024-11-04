from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.DataScenarioManager import data_scenario_manager_instance, ScenarioNotFoundError
from app.api.dto.ResponseDSC import ResponseDSC

router = APIRouter()

class RequestCreateRunningScenario(BaseModel):
    scenario_name: str

class ResponseCreateRunningScenario(BaseModel):
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
    except ScenarioNotFoundError:
        raise HTTPException(status_code=404, detail="Scenario not found")


class DataScenarioExecutorDto(BaseModel):
    name: str
    description: str
    conda_environment: str
    script_path: str
    uid: str


class DataScenarioExecutorListDto(BaseModel):
    data_scenario_executor_list: list[DataScenarioExecutorDto]


from app.entities.DataScenarioExecutor import DataScenarioExecutor


def convert_data_scenario_executor_to_data_scenario_executor_dto(data_scenario_executor: DataScenarioExecutor):
    return DataScenarioExecutorDto(
        name=data_scenario_executor.data_scenario.name,
        description=data_scenario_executor.data_scenario.description,
        conda_environment=data_scenario_executor.data_scenario.conda_environment,
        script_path=data_scenario_executor.data_scenario.script_path_str,
        uid=data_scenario_executor.uid_str,
    )


@router.get("/running-scenarios", response_model=ResponseDSC[DataScenarioExecutorListDto])
def get_data_scenarios_running():
    data_scenario_executor_list = list(
        map(convert_data_scenario_executor_to_data_scenario_executor_dto,
            list(data_scenario_manager_instance.get_data_scenario_executor_dict().values())
            )
    )
    return ResponseDSC(
        success=True,
        data=DataScenarioExecutorListDto(data_scenario_executor_list=data_scenario_executor_list)
    )


@router.get("/running-scenarios/{running_uid}")
def get_data_scenario_running(running_uid: str):
    try:
        return convert_data_scenario_executor_to_data_scenario_executor_dto(
            data_scenario_manager_instance.get_data_scenario_executor(running_uid)
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="scenario not found")


# 시나리오 정지
@router.post("/running-scenarios/{running_uid}/stop")
def stop_scenario(running_uid: str):
    data_scenario_manager_instance.stop_scenario(running_uid)
    return {"message": "Request to stop scenario"}


@router.post("/running-scenarios/{running_uid}/kill")
def stop_scenario(running_uid: str):
    data_scenario_manager_instance.stop_scenario(running_uid)
    return {"message": "Request to kill scenario"}
