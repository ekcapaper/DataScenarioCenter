import subprocess
import threading

from app.entities.DataScenario import DataScenario
import os

class DataScenarioExecutor(threading.Thread):
    def __init__(self, data_scenario: DataScenario):
        super().__init__()
        self.__data_scenario = data_scenario
        self.__is_running = False
        self.__is_started = False
        self.__popen_instance = None
        self.__uid = None

    def run(self):
        script_to_run = self.__data_scenario.script_path_str
        command = f"conda run -n {self.__data_scenario.conda_environment} python {script_to_run}"
        self.__popen_instance = subprocess.Popen(command, shell=True)
        self.__is_running = True
        self.__is_started = True
        self.__uid = self.__popen_instance.pid
        self.__popen_instance.wait()

        # 프로세스가 완료될 때까지 기다리고 결과를 받음
        stdout, stderr = self.__popen_instance.communicate()

        # 종료 코드 확인
        return_code = self.__popen_instance.returncode

        #print(f"표준 출력: {stdout}")
        #print(f"표준 에러: {stderr}")
        #print(f"종료 코드: {return_code}")

    def stop(self):
        self.request_stop()

    def request_stop(self):
        self.__popen_instance.terminate()

    def stop_force(self):
        self.__popen_instance.kill()

    @property
    def is_running(self):
        if self.__popen_instance is None:
            self.__is_running = False
        elif self.__popen_instance.poll() is not None:
            self.__is_running = False
        return self.__is_running

    @property
    def uid_str(self):
        return str(self.__uid)

    @property
    def data_scenario(self):
        return self.__data_scenario

    @property
    def is_started(self):
        return self.__is_started
