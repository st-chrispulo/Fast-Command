from job.executors.base_executor import BaseExecutor
from logger import logger


class RetryingExecutor(BaseExecutor):
    def run(self):
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                logger.info(f"[Executor] Attempt {attempt} for command '{self.command_name}'")
                command_class = self._get_command_class()
                return command_class(self.payload).run()
            except Exception as e:
                logger.warning(f"[Executor] Attempt {attempt} failed: {e}")
                if attempt == max_attempts:
                    raise
