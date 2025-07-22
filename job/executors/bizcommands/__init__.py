from job.executors.bizcommands.run_report import RunReportCommand
from job.executors.bizcommands.generate_invoice import GenerateInvoiceCommand
from job.executors.bizcommands.socket_event_checkpoint import SocketEventCheckpointCommand
from job.executors.bizcommands.long_running_biz_case import LongRunningBusinessCaseCommand


command_registry = {
    "run_report": RunReportCommand,
    "generate_invoice": GenerateInvoiceCommand,
    "socket_event_checkpoint": SocketEventCheckpointCommand,
    "long_running_biz_case": LongRunningBusinessCaseCommand
}
