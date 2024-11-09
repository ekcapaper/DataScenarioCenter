import signal
import subprocess

from app.entities.DataScenario import DataScenario
from threading import Thread
from app.exceptions.AlreadyStartedException import AlreadyStartedException
from app.exceptions.FailedKillException import FailedKillException


class DataScenarioExecutor:
    def __init__(self, data_scenario: DataScenario):
        super().__init__()
        self.__data_scenario = data_scenario
        self.__executor = None

    @property
    def data_scenario(self):
        return self.__data_scenario

    @property
    def is_running(self):
        if self.__executor is None:
            return False
        else:
            return True

    def __run_data_scenario(self):
        command = f"conda run -n {self.__data_scenario.conda_environment} python {self.__data_scenario.script_path_str}"
        # popen 객체 생성
        self.__popen_instance = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # popen 대기
        self.__popen_instance.wait()

    def start(self):
        if self.__executor is None:
            self.__executor = Thread(target=self.__run_data_scenario)
            self.__executor.start()
        else:
            raise AlreadyStartedException("Executor already started")

    async def stop(self):
        if self.__executor is None:
            return True

        # request terminate
        self.__executor.terminate()
        for i in range(10):
            if not self.__popen_instance.poll() is None:
                self.__executor = None
                return True

        # request kill
        self.__popen_instance.kill()
        for i in range(10):
            if not self.__popen_instance.poll() is None:
                self.__executor = None
                return True

        # Failed
        raise FailedKillException()
