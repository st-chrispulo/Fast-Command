from abc import ABC, abstractmethod
from job.executors.bizcommands import command_registry


class BaseExecutor(ABC):
    def __init__(self, command_name: str, payload: dict):
        self.command_name = command_name
        self.payload = payload

    @abstractmethod
    def run(self):
        pass

    def _get_command_class(self):
        if self.command_name not in command_registry:
            raise ValueError(f"Command '{self.command_name}' is not implemented")
        return command_registry[self.command_name]
