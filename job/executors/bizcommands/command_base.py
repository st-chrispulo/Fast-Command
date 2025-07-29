from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, payload, pg_connection=None):
        self.payload = payload
        self.pg_connection = pg_connection

    @abstractmethod
    def run(self):
        pass
