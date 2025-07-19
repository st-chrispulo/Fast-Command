from job.executors.bizcommands import command_registry


def execute_job(command_name: str, payload: dict):
    if command_name not in command_registry:
        raise ValueError(f"Command '{command_name}' is not implemented")

    command_class = command_registry[command_name]
    command_instance = command_class(payload)
    return command_instance.run()
